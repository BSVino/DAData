#include "lmdb_helper.h"

LMDBDatabase::LMDBDatabase(const tstring& database)
{
	m_dbi = 0;
	m_env = nullptr;
	m_transaction = nullptr;
	m_valid = false;

	if (mdb_env_create(&m_env) != 0)
	{
		m_valid = false;
		return;
	}

	if (mdb_env_set_maxdbs(m_env, 2) != 0)
	{
		m_valid = false;
		return;
	}

	// 500 megabytes and change should be more than I'll ever need.
	if (mdb_env_set_mapsize(m_env, 4096 * 1024 * 128) != 0)
	{
		m_valid = false;
		return;
	}

	if (mdb_env_open(m_env, database.c_str(), 0, 0664) != 0)
	{
		m_valid = false;
		return;
	}

	m_valid = true;
}

LMDBDatabase::~LMDBDatabase()
{
	CloseDatabase();

	mdb_env_close(m_env);
}

bool LMDBDatabase::IsValid() const
{
	return m_valid;
}

bool LMDBDatabase::OpenDatabase(const char* database_name, int flags)
{
	if (!IsValid())
		return false;

	if (m_dbi)
	{
		if (!CloseDatabase())
			return false;
	}

	if (mdb_txn_begin(m_env, NULL, 0, &m_transaction) != 0)
	{
		m_transaction = nullptr;
		return false;
	}

	if (mdb_dbi_open(m_transaction, database_name, flags, &m_dbi) != 0)
	{
		mdb_txn_abort(m_transaction);
		m_transaction = nullptr;
		return false;
	}

	return true;
}

bool LMDBDatabase::CloseDatabase()
{
	if (!IsValid())
		return false;

	if (m_transaction)
		mdb_txn_commit(m_transaction);

	m_transaction = nullptr;

	mdb_dbi_close(m_env, m_dbi);
	m_dbi = 0;

	return true;
}

MDB_val LMDBDatabase::MakeKey(int& key)
{
	MDB_val db_key;
	db_key.mv_size = sizeof(key);
	db_key.mv_data = &key;
	return db_key;
}

MDB_val LMDBDatabase::MakeKey(const tstring& key)
{
	MDB_val db_key;
	db_key.mv_size = key.length();
	db_key.mv_data = (void*)key.data();
	return db_key;
}

bool LMDBDatabase::GetRecord(int key, google::protobuf::Message& data)
{
	return GetRecord(MakeKey(key), data);
}

bool LMDBDatabase::GetRecord(const tstring& key, google::protobuf::Message& data)
{
	return GetRecord(MakeKey(key), data);
}

bool LMDBDatabase::GetRecord(const MDB_val& db_key, google::protobuf::Message& data)
{
	if (!IsValid())
		return false;

	MDB_val db_data;

	if (mdb_get(m_transaction, m_dbi, const_cast<MDB_val*>(&db_key), &db_data) != 0)
		return false;

	data.ParseFromArray(db_data.mv_data, db_data.mv_size);

	return true;
}

bool LMDBDatabase::SetRecord(int key, const google::protobuf::Message& data)
{
	return SetRecord(MakeKey(key), data);
}

bool LMDBDatabase::SetRecord(const tstring& key, const google::protobuf::Message& data)
{
	return SetRecord(MakeKey(key), data);
}

bool LMDBDatabase::SetRecord(const MDB_val& db_key, const google::protobuf::Message& data)
{
	if (!IsValid())
		return false;

	MDB_val db_data;

	std::string data_serialized = data.SerializeAsString();

	db_data.mv_size = data_serialized.length();
	db_data.mv_data = (void*)data_serialized.data();

	int result = mdb_put(m_transaction, m_dbi, const_cast<MDB_val*>(&db_key), &db_data, 0);

	if (result == MDB_MAP_FULL)
		puts("Put failed because map is full. Increase map size.\n");

	if (result != 0)
		return false;

	return true;
}
