#include <time.h>

#include "../protobuf-cpp/data.pb.h"
#include "../database/database.pb.h"

#include <tstring.h>

#include "getopt.h" // "" and not <> so we grab the local one so this code can run on win32

#include "../database/lmdb_helper.h"

using namespace std;

#ifdef _DEBUG
#define Assert(x) \
{ \
	if (!(x)) \
		{ \
		TDebugBreak(); \
		} \
}
#else
#define Assert(x)
#endif

#define Die(reason) \
{ \
	puts(reason); \
	return false; \
} \

bool DumpDatabase(tstring database)
{
	if (!database.length())
		Die("No database specified!\n");

	LMDBDatabase db(database);

	puts("Players:\n");
	db.OpenDatabase("players", MDB_INTEGERKEY);

	MDB_cursor* cursor;
	mdb_cursor_open(db.m_transaction, db.m_dbi, &cursor);

	MDB_val key, data;
	da::protobuf::players_entry pb_player;

	while ((mdb_cursor_get(cursor, &key, &data, MDB_NEXT)) == 0)
	{
		pb_player.ParseFromArray(data.mv_data, data.mv_size);
		printf("Key: %d\n\n", *(int*)key.mv_data);
		pb_player.PrintDebugString();
		puts("\n\n\n");
	}

	mdb_cursor_close(cursor);

	db.CloseDatabase();

	puts("Leaders:\n");
	db.OpenDatabase("leaders", 0);

	mdb_cursor_open(db.m_transaction, db.m_dbi, &cursor);

	da::protobuf::leaders_entry pb_leader;

	while ((mdb_cursor_get(cursor, &key, &data, MDB_NEXT)) == 0)
	{
		printf("Key: %s\n\n", key.mv_data);
		pb_leader.ParseFromArray(data.mv_data, data.mv_size);
		pb_leader.PrintDebugString();
		puts("\n\n\n");
	}

	mdb_cursor_close(cursor);

	db.CloseDatabase();

	return true;
}

struct player_style
{
	unsigned int account;
	float style;
};

bool style_compare(const player_style& l, const player_style& r)
{
	return l.style < r.style;
}

bool CalculateLeaders(tstring database)
{
	if (!database.length())
		Die("No database specified!\n");

	LMDBDatabase db(database);

	tvector<player_style> daily_leaders;
	tvector<player_style> weekly_leaders;
	tvector<player_style> monthly_leaders;

	db.OpenDatabase("players", MDB_INTEGERKEY);

	MDB_cursor* cursor;
	mdb_cursor_open(db.m_transaction, db.m_dbi, &cursor);

	MDB_val key, data;
	da::protobuf::players_entry pb_player;

	while ((mdb_cursor_get(cursor, &key, &data, MDB_NEXT)) == 0)
	{
		pb_player.ParseFromArray(data.mv_data, data.mv_size);
		Assert(*(int*)key.mv_data == pb_player.account_id());

		if (pb_player.daily_style() > 0)
		{
			auto& daily_player = daily_leaders.push_back();
			daily_player.account = pb_player.account_id();
			daily_player.style = pb_player.daily_style();
		}

		if (pb_player.weekly_style() > 0)
		{
			auto& weekly_player = weekly_leaders.push_back();
			weekly_player.account = pb_player.account_id();
			weekly_player.style = pb_player.weekly_style();
		}
		
		if (pb_player.monthly_style() > 0)
		{
			auto& monthly_player = monthly_leaders.push_back();
			monthly_player.account = pb_player.account_id();
			monthly_player.style = pb_player.monthly_style();
		}
	}

	mdb_cursor_close(cursor);

	db.CloseDatabase();

	// These should be O(n)
	make_heap(daily_leaders.begin(), daily_leaders.end(), style_compare);
	make_heap(weekly_leaders.begin(), weekly_leaders.end(), style_compare);
	make_heap(monthly_leaders.begin(), monthly_leaders.end(), style_compare);

	da::protobuf::leaders_entry pb_daily_leaders;
	da::protobuf::leaders_entry pb_weekly_leaders;
	da::protobuf::leaders_entry pb_monthly_leaders;

	pb_daily_leaders.mutable_leaders()->Reserve(100);
	pb_weekly_leaders.mutable_leaders()->Reserve(100);
	pb_monthly_leaders.mutable_leaders()->Reserve(100);

	// This is O(n log n) but we only do it for 100 elements each
	for (int i = 0; i < 100; i++)
	{
		if (daily_leaders.size())
		{
			*pb_daily_leaders.mutable_leaders()->AddAlreadyReserved() = daily_leaders.front().account;

			pop_heap(daily_leaders.begin(), daily_leaders.end(), style_compare);
			daily_leaders.pop_back();
		}

		if (weekly_leaders.size())
		{
			*pb_weekly_leaders.mutable_leaders()->AddAlreadyReserved() = weekly_leaders.front().account;

			pop_heap(weekly_leaders.begin(), weekly_leaders.end(), style_compare);
			weekly_leaders.pop_back();
		}

		if (monthly_leaders.size())
		{
			*pb_monthly_leaders.mutable_leaders()->AddAlreadyReserved() = monthly_leaders.front().account;

			pop_heap(monthly_leaders.begin(), monthly_leaders.end(), style_compare);
			monthly_leaders.pop_back();
		}

		if (!daily_leaders.size() || !weekly_leaders.size() || !monthly_leaders.size())
			break;
	}

	db.OpenDatabase("leaders", 0);

	db.SetRecord("daily", pb_daily_leaders);
	db.SetRecord("weekly", pb_weekly_leaders);
	db.SetRecord("monthly", pb_monthly_leaders);

	db.CloseDatabase();

	return true;
}

bool StoreDataToDatabase(da::protobuf::GameData& pb_gamedata, tstring database, tstring& output)
{
	if (!database.length())
		Die("No database specified!\n");

	LMDBDatabase db(database);

	if (!db.IsValid())
		Die("Couldn't open database file.\n");

	if (pb_gamedata.player_list().size())
	{
		if (!db.OpenDatabase("players", MDB_INTEGERKEY | MDB_CREATE))
			Die("Couldn't open players database\n");

		for (int i = 0; i < pb_gamedata.player_list().size(); i++)
		{
			const auto& pb_player = pb_gamedata.player_list(i);

			auto account_id = pb_player.accountid();

			da::protobuf::players_entry pb_players_entry;

			if (!db.GetRecord(account_id, pb_players_entry))
			{
				pb_players_entry.set_account_id(account_id);
				pb_players_entry.set_name(pb_player.name());
			}
			Assert(account_id == pb_players_entry.account_id());

			pb_players_entry.set_daily_style(pb_players_entry.daily_style() + pb_player.style());
			pb_players_entry.set_weekly_style(pb_players_entry.weekly_style() + pb_player.style());
			pb_players_entry.set_monthly_style(pb_players_entry.monthly_style() + pb_player.style());

			if (!db.SetRecord(account_id, pb_players_entry))
				Die("Error putting data.\n");
		}

		db.CloseDatabase();
	}

	int daily_leader = 0;
	int weekly_leader = 0;
	int monthly_leader = 0;

	if (!db.OpenDatabase("leaders", MDB_CREATE))
		Die("Couldn't open leaders database\n");

	da::protobuf::leaders_entry pb_leaders;
	if (db.GetRecord("daily", pb_leaders))
	{
		if (pb_leaders.leaders().size())
			daily_leader = pb_leaders.leaders(0);
	}

	if (db.GetRecord("weekly", pb_leaders))
	{
		if (pb_leaders.leaders().size())
			weekly_leader = pb_leaders.leaders(0);
	}

	if (db.GetRecord("monthly", pb_leaders))
	{
		if (pb_leaders.leaders().size())
			monthly_leader = pb_leaders.leaders(0);
	}

	db.CloseDatabase();

	da::protobuf::ServerReply pb_serverreply;

	if (!db.OpenDatabase("players", MDB_INTEGERKEY | MDB_CREATE))
		Die("Couldn't open players database\n");

	da::protobuf::players_entry pb_playerentry;

	if (daily_leader && db.GetRecord(daily_leader, pb_playerentry))
	{
		Assert(daily_leader == pb_playerentry.account_id());
		pb_serverreply.set_daily_leader(pb_playerentry.name());
		pb_serverreply.set_daily_leader_style(pb_playerentry.daily_style());
	}

	if (weekly_leader && db.GetRecord(weekly_leader, pb_playerentry))
	{
		Assert(weekly_leader == pb_playerentry.account_id());
		pb_serverreply.set_weekly_leader(pb_playerentry.name());
		pb_serverreply.set_weekly_leader_style(pb_playerentry.weekly_style());
	}

	if (monthly_leader && db.GetRecord(monthly_leader, pb_playerentry))
	{
		Assert(monthly_leader == pb_playerentry.account_id());
		pb_serverreply.set_monthly_leader(pb_playerentry.name());
		pb_serverreply.set_monthly_leader_style(pb_playerentry.monthly_style());
	}

	output = pb_serverreply.SerializeAsString();

	db.CloseDatabase();

	return true;
}

bool ResetStyles(tstring database, bool daily, bool weekly, bool monthly)
{
	if (!database.length())
		Die("No database specified!\n");

	LMDBDatabase db(database);

	if (!db.IsValid())
		Die("Couldn't open database file.\n");

	if (!db.OpenDatabase("players", MDB_INTEGERKEY))
		Die("Couldn't open players database\n");

	MDB_stat stat;
	mdb_env_stat(db.m_env, &stat);

	MDB_cursor* cursor;
	mdb_cursor_open(db.m_transaction, db.m_dbi, &cursor);

	MDB_val key, data;
	da::protobuf::players_entry pb_player;

	while ((mdb_cursor_get(cursor, &key, &data, MDB_NEXT)) == 0)
	{
		pb_player.ParseFromArray(data.mv_data, data.mv_size);

		Assert(*(int*)key.mv_data == pb_player.account_id());

		if (daily)
			pb_player.clear_daily_style();

		if (weekly)
			pb_player.clear_weekly_style();

		if (monthly)
			pb_player.clear_monthly_style();

		db.SetRecord(pb_player.account_id(), pb_player);
	}

	mdb_cursor_close(cursor);

	db.CloseDatabase();

	return true;
}

#undef Die

int main(int argc, char** args)
{
	tstring database;

	int opt;
	while ((opt = getopt(argc, args, "td:")) >= 0)
	{
		switch (opt)
		{
		case 'd':
			database = optarg;
			break;

		default:
			break;
		}
	}

	if (optind >= argc)
	{
		printf("Commands: store [file], dump, calc_leaders");
		return 1;
	}

	if (tstring("dump") == args[optind])
	{
		return DumpDatabase(database) ? 0 : 1;
	}
	else if (tstring("calc_leaders") == args[optind])
	{
		return CalculateLeaders(database) ? 0 : 1;
	}
	else if (tstring("reset_daily") == args[optind])
	{
		return ResetStyles(database, true, false, false) ? 0 : 1;
	}
	else if (tstring("reset_weekly") == args[optind])
	{
		return ResetStyles(database, true, true, false) ? 0 : 1;
	}
	else if (tstring("reset_monthly") == args[optind])
	{
		return ResetStyles(database, true, true, true) ? 0 : 1;
	}
	else if (tstring("store") == args[optind])
	{
		optind += 1;

		string data;

		if (optind >= argc)
		{
#define BUFFER_SIZE 1024
			char szBuffer[BUFFER_SIZE];

			for (;;)
			{
				size_t bytes = fread(szBuffer, 1, BUFFER_SIZE, stdin);

				if (bytes < BUFFER_SIZE && feof(stdin))
					break;

				data.append(szBuffer);
			}
		}
		else
		{
			FILE* fp = fopen(args[optind], "r");

			fseek(fp, 0, SEEK_END);
			data.resize(ftell(fp) + 1);
			fseek(fp, 0, SEEK_SET);
			fread((char*)data.data(), 1, data.size() - 1, fp);
			fclose(fp);
		}

		da::protobuf::GameData pb_gamedata;
		pb_gamedata.ParseFromString(data);

		tstring output;
		StoreDataToDatabase(pb_gamedata, database, output) ? 0 : 1;

		puts(output.c_str());
	}
#ifdef _DEBUG
	else if (tstring("make_test") == args[optind])
	{
		da::protobuf::GameData* pb_gamedata = new da::protobuf::GameData();

		auto pb_player1 = pb_gamedata->mutable_player_list()->Add();
		pb_player1->set_accountid(1234);
		pb_player1->set_name("Test Player 1");
		pb_player1->set_style(1234);

		auto pb_player2 = pb_gamedata->mutable_player_list()->Add();
		pb_player2->set_accountid(2345);
		pb_player2->set_name("Test Player 2");
		pb_player2->set_style(2345);

		auto pb_player3 = pb_gamedata->mutable_player_list()->Add();
		pb_player3->set_accountid(3456);
		pb_player3->set_name("Test Player 3");
		pb_player3->set_style(3456);

		string gamedata = pb_gamedata->SerializeAsString();

		FILE* fp = fopen("test-data.pb", "w");
		fwrite(gamedata.data(), gamedata.length(), 1, fp);
		fclose(fp);
	}
	else if (tstring("db_stress_insert") == args[optind])
	{
		srand(0);
		da::protobuf::GameData pb_gamedata;

		int days = 62;
		for (int d = 1; d < days; d++)
		{
			int games = rand() % 50 + 20;
			for (int g = 0; g < games; g++)
			{
				pb_gamedata.Clear();

				int max_players = rand() % 8 + 8;
				for (int j = 0; j < max_players; j++)
				{
					auto pb_player = pb_gamedata.mutable_player_list()->Add();
					pb_player->set_accountid(rand() % 10000000);
					pb_player->set_style((float)(rand() % 1000 + 1000));
					pb_player->set_name(sprintf(tstring("Player %d"), pb_player->accountid()));
				}

				StoreDataToDatabase(pb_gamedata, database, tstring());

				CalculateLeaders(database);
			}

			if (d % 30 == 0)
				ResetStyles(database, true, true, true);
			else if (d % 7 == 0)
				ResetStyles(database, true, true, false);
			else
				ResetStyles(database, true, false, false);
		}
	}
#endif
	else
	{
		printf("Don't know that command.\n");
		return 1;
	}

	return 0;
}
