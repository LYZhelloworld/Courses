#include "simulator.h"
#include "two_bit_branch_predictor.h"

TwoBitBranchPredictor::TwoBitBranchPredictor(String name, core_id_t core_id, UInt32 size)
   : BranchPredictor(name, core_id)
   , m_bits(size)
{
}

TwoBitBranchPredictor::~TwoBitBranchPredictor()
{
}

bool TwoBitBranchPredictor::predict(IntPtr ip, IntPtr target)
{
   UInt32 index = ip % m_bits.size();
   return get_from_state(m_bits[index]);
}

void TwoBitBranchPredictor::update(bool predicted, bool actual, IntPtr ip, IntPtr target)
{
   updateCounters(predicted, actual);
   UInt32 index = ip % m_bits.size();
   m_bits[index] = update_state(m_bits[index], actual);
}