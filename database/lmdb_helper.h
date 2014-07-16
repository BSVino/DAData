#pragma once

#include <lmdb.h>

#include <tstring.h>

#include "../database/database.pb.h"

// Some RAII up in this shit.
class LMDBDatabase
{
public:
	bool m_valid;

	MDB_env* m_env;
	MDB_dbi  m_dbi;
	MDB_txn* m_transaction;

public:
	LMDBDatabase(const tstring& database);
	~LMDBDatabase();

	bool IsValid() const;

	bool OpenDatabase(const char* database_name = nullptr, int flags = 0);
	bool CloseDatabase();

	MDB_val MakeKey(int& key);
	MDB_val MakeKey(const tstring& key);

	bool GetRecord(int key, google::protobuf::Message& data);
	bool GetRecord(const tstring& key, google::protobuf::Message& data);
	bool GetRecord(const MDB_val& db_key, google::protobuf::Message& data);

	bool GetRecord(int key, std::string& data);
	bool GetRecord(const tstring& key, std::string& data);
	bool GetRecord(const MDB_val& db_key, std::string& data);

	bool SetRecord(int key, const google::protobuf::Message& data);
	bool SetRecord(const tstring& key, const google::protobuf::Message& data);
	bool SetRecord(const MDB_val& db_key, const google::protobuf::Message& data);
};
