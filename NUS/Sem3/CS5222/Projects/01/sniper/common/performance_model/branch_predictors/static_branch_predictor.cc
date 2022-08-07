#include "simulator.h"
#include "static_branch_predictor.h"

StaticBranchPredictor::StaticBranchPredictor(String name, core_id_t core_id)
   : BranchPredictor(name, core_id)
{
}

StaticBranchPredictor::~StaticBranchPredictor()
{
}

bool StaticBranchPredictor::predict(IntPtr ip, IntPtr target)
{
   return true;
}

void StaticBranchPredictor::update(bool predicted, bool actual, IntPtr ip, IntPtr target)
{
   updateCounters(predicted, actual);
}
