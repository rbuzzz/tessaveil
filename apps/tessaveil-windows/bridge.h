#pragma once
#include <cstddef>
#include <cstdint>
// ABI 1: synchronous, disjoint writable buffers; Rust wipes all input fields.
// Handle is Rust-owned; destroy exactly once. No foreign exceptions may cross.
struct TvInput {
  uint32_t len[4]{};
  uint8_t data[4][4096]{};
};
struct TvReply {
  uint32_t abi{}, state{}, dirty{}, sheets{}, rows{}, columns{},
      protected_sheet{}, verified{}, minutes{}, text_len{};
  uint8_t text[4096]{};
};
static_assert(sizeof(TvInput) == 16400 && sizeof(TvReply) == 4136);
static_assert(offsetof(TvReply, text) == 40 && offsetof(TvInput, data) == 16);
extern "C" {
uint64_t tv_new();
void tv_free(uint64_t);
int32_t tv_call(uint64_t, uint32_t, uint32_t, uint32_t, TvInput *, TvReply *);
}
enum Operation : uint32_t {
  Ack = 1,
  Create,
  Open,
  Save,
  Close,
  Lock,
  Unlock,
  Add,
  Select,
  Verify,
  SetSheetPassword,
  Protect,
  UnlockSheet,
  UnlockMaster,
  Spin,
  Timeout,
  Activity,
  Tick,
  Info,
  Cell,
  Profile,
  ProfileCount,
  SheetName
};
