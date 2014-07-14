// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: database.proto

#ifndef PROTOBUF_database_2eproto__INCLUDED
#define PROTOBUF_database_2eproto__INCLUDED

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 2005000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 2005000 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)

namespace da {
namespace protobuf {

// Internal implementation detail -- do not call these.
void  protobuf_AddDesc_database_2eproto();
void protobuf_AssignDesc_database_2eproto();
void protobuf_ShutdownFile_database_2eproto();

class players_entry;
class leaders_entry;

// ===================================================================

class players_entry : public ::google::protobuf::Message {
 public:
  players_entry();
  virtual ~players_entry();

  players_entry(const players_entry& from);

  inline players_entry& operator=(const players_entry& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const players_entry& default_instance();

  void Swap(players_entry* other);

  // implements Message ----------------------------------------------

  players_entry* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const players_entry& from);
  void MergeFrom(const players_entry& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:

  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // optional float daily_style = 1;
  inline bool has_daily_style() const;
  inline void clear_daily_style();
  static const int kDailyStyleFieldNumber = 1;
  inline float daily_style() const;
  inline void set_daily_style(float value);

  // optional float weekly_style = 2;
  inline bool has_weekly_style() const;
  inline void clear_weekly_style();
  static const int kWeeklyStyleFieldNumber = 2;
  inline float weekly_style() const;
  inline void set_weekly_style(float value);

  // optional float monthly_style = 3;
  inline bool has_monthly_style() const;
  inline void clear_monthly_style();
  static const int kMonthlyStyleFieldNumber = 3;
  inline float monthly_style() const;
  inline void set_monthly_style(float value);

  // optional int32 account_id = 4;
  inline bool has_account_id() const;
  inline void clear_account_id();
  static const int kAccountIdFieldNumber = 4;
  inline ::google::protobuf::int32 account_id() const;
  inline void set_account_id(::google::protobuf::int32 value);

  // optional string name = 5;
  inline bool has_name() const;
  inline void clear_name();
  static const int kNameFieldNumber = 5;
  inline const ::std::string& name() const;
  inline void set_name(const ::std::string& value);
  inline void set_name(const char* value);
  inline void set_name(const char* value, size_t size);
  inline ::std::string* mutable_name();
  inline ::std::string* release_name();
  inline void set_allocated_name(::std::string* name);

  // @@protoc_insertion_point(class_scope:da.protobuf.players_entry)
 private:
  inline void set_has_daily_style();
  inline void clear_has_daily_style();
  inline void set_has_weekly_style();
  inline void clear_has_weekly_style();
  inline void set_has_monthly_style();
  inline void clear_has_monthly_style();
  inline void set_has_account_id();
  inline void clear_has_account_id();
  inline void set_has_name();
  inline void clear_has_name();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  float daily_style_;
  float weekly_style_;
  float monthly_style_;
  ::google::protobuf::int32 account_id_;
  ::std::string* name_;

  mutable int _cached_size_;
  ::google::protobuf::uint32 _has_bits_[(5 + 31) / 32];

  friend void  protobuf_AddDesc_database_2eproto();
  friend void protobuf_AssignDesc_database_2eproto();
  friend void protobuf_ShutdownFile_database_2eproto();

  void InitAsDefaultInstance();
  static players_entry* default_instance_;
};
// -------------------------------------------------------------------

class leaders_entry : public ::google::protobuf::Message {
 public:
  leaders_entry();
  virtual ~leaders_entry();

  leaders_entry(const leaders_entry& from);

  inline leaders_entry& operator=(const leaders_entry& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const leaders_entry& default_instance();

  void Swap(leaders_entry* other);

  // implements Message ----------------------------------------------

  leaders_entry* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const leaders_entry& from);
  void MergeFrom(const leaders_entry& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:

  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // repeated int32 leaders = 1;
  inline int leaders_size() const;
  inline void clear_leaders();
  static const int kLeadersFieldNumber = 1;
  inline ::google::protobuf::int32 leaders(int index) const;
  inline void set_leaders(int index, ::google::protobuf::int32 value);
  inline void add_leaders(::google::protobuf::int32 value);
  inline const ::google::protobuf::RepeatedField< ::google::protobuf::int32 >&
      leaders() const;
  inline ::google::protobuf::RepeatedField< ::google::protobuf::int32 >*
      mutable_leaders();

  // @@protoc_insertion_point(class_scope:da.protobuf.leaders_entry)
 private:

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::RepeatedField< ::google::protobuf::int32 > leaders_;

  mutable int _cached_size_;
  ::google::protobuf::uint32 _has_bits_[(1 + 31) / 32];

  friend void  protobuf_AddDesc_database_2eproto();
  friend void protobuf_AssignDesc_database_2eproto();
  friend void protobuf_ShutdownFile_database_2eproto();

  void InitAsDefaultInstance();
  static leaders_entry* default_instance_;
};
// ===================================================================


// ===================================================================

// players_entry

// optional float daily_style = 1;
inline bool players_entry::has_daily_style() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void players_entry::set_has_daily_style() {
  _has_bits_[0] |= 0x00000001u;
}
inline void players_entry::clear_has_daily_style() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void players_entry::clear_daily_style() {
  daily_style_ = 0;
  clear_has_daily_style();
}
inline float players_entry::daily_style() const {
  return daily_style_;
}
inline void players_entry::set_daily_style(float value) {
  set_has_daily_style();
  daily_style_ = value;
}

// optional float weekly_style = 2;
inline bool players_entry::has_weekly_style() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void players_entry::set_has_weekly_style() {
  _has_bits_[0] |= 0x00000002u;
}
inline void players_entry::clear_has_weekly_style() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void players_entry::clear_weekly_style() {
  weekly_style_ = 0;
  clear_has_weekly_style();
}
inline float players_entry::weekly_style() const {
  return weekly_style_;
}
inline void players_entry::set_weekly_style(float value) {
  set_has_weekly_style();
  weekly_style_ = value;
}

// optional float monthly_style = 3;
inline bool players_entry::has_monthly_style() const {
  return (_has_bits_[0] & 0x00000004u) != 0;
}
inline void players_entry::set_has_monthly_style() {
  _has_bits_[0] |= 0x00000004u;
}
inline void players_entry::clear_has_monthly_style() {
  _has_bits_[0] &= ~0x00000004u;
}
inline void players_entry::clear_monthly_style() {
  monthly_style_ = 0;
  clear_has_monthly_style();
}
inline float players_entry::monthly_style() const {
  return monthly_style_;
}
inline void players_entry::set_monthly_style(float value) {
  set_has_monthly_style();
  monthly_style_ = value;
}

// optional int32 account_id = 4;
inline bool players_entry::has_account_id() const {
  return (_has_bits_[0] & 0x00000008u) != 0;
}
inline void players_entry::set_has_account_id() {
  _has_bits_[0] |= 0x00000008u;
}
inline void players_entry::clear_has_account_id() {
  _has_bits_[0] &= ~0x00000008u;
}
inline void players_entry::clear_account_id() {
  account_id_ = 0;
  clear_has_account_id();
}
inline ::google::protobuf::int32 players_entry::account_id() const {
  return account_id_;
}
inline void players_entry::set_account_id(::google::protobuf::int32 value) {
  set_has_account_id();
  account_id_ = value;
}

// optional string name = 5;
inline bool players_entry::has_name() const {
  return (_has_bits_[0] & 0x00000010u) != 0;
}
inline void players_entry::set_has_name() {
  _has_bits_[0] |= 0x00000010u;
}
inline void players_entry::clear_has_name() {
  _has_bits_[0] &= ~0x00000010u;
}
inline void players_entry::clear_name() {
  if (name_ != &::google::protobuf::internal::kEmptyString) {
    name_->clear();
  }
  clear_has_name();
}
inline const ::std::string& players_entry::name() const {
  return *name_;
}
inline void players_entry::set_name(const ::std::string& value) {
  set_has_name();
  if (name_ == &::google::protobuf::internal::kEmptyString) {
    name_ = new ::std::string;
  }
  name_->assign(value);
}
inline void players_entry::set_name(const char* value) {
  set_has_name();
  if (name_ == &::google::protobuf::internal::kEmptyString) {
    name_ = new ::std::string;
  }
  name_->assign(value);
}
inline void players_entry::set_name(const char* value, size_t size) {
  set_has_name();
  if (name_ == &::google::protobuf::internal::kEmptyString) {
    name_ = new ::std::string;
  }
  name_->assign(reinterpret_cast<const char*>(value), size);
}
inline ::std::string* players_entry::mutable_name() {
  set_has_name();
  if (name_ == &::google::protobuf::internal::kEmptyString) {
    name_ = new ::std::string;
  }
  return name_;
}
inline ::std::string* players_entry::release_name() {
  clear_has_name();
  if (name_ == &::google::protobuf::internal::kEmptyString) {
    return NULL;
  } else {
    ::std::string* temp = name_;
    name_ = const_cast< ::std::string*>(&::google::protobuf::internal::kEmptyString);
    return temp;
  }
}
inline void players_entry::set_allocated_name(::std::string* name) {
  if (name_ != &::google::protobuf::internal::kEmptyString) {
    delete name_;
  }
  if (name) {
    set_has_name();
    name_ = name;
  } else {
    clear_has_name();
    name_ = const_cast< ::std::string*>(&::google::protobuf::internal::kEmptyString);
  }
}

// -------------------------------------------------------------------

// leaders_entry

// repeated int32 leaders = 1;
inline int leaders_entry::leaders_size() const {
  return leaders_.size();
}
inline void leaders_entry::clear_leaders() {
  leaders_.Clear();
}
inline ::google::protobuf::int32 leaders_entry::leaders(int index) const {
  return leaders_.Get(index);
}
inline void leaders_entry::set_leaders(int index, ::google::protobuf::int32 value) {
  leaders_.Set(index, value);
}
inline void leaders_entry::add_leaders(::google::protobuf::int32 value) {
  leaders_.Add(value);
}
inline const ::google::protobuf::RepeatedField< ::google::protobuf::int32 >&
leaders_entry::leaders() const {
  return leaders_;
}
inline ::google::protobuf::RepeatedField< ::google::protobuf::int32 >*
leaders_entry::mutable_leaders() {
  return &leaders_;
}


// @@protoc_insertion_point(namespace_scope)

}  // namespace protobuf
}  // namespace da

#ifndef SWIG
namespace google {
namespace protobuf {


}  // namespace google
}  // namespace protobuf
#endif  // SWIG

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_database_2eproto__INCLUDED
