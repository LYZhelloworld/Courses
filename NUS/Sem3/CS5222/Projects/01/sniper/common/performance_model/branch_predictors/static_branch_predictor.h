#ifndef STATIC_BRANCH_PREDICTOR_H
#define STATIC_BRANCH_PREDICTOR_H

#include "branch_predictor.h"

#include <vector>

class StaticBranchPredictor : public BranchPredictor
{
public:
   StaticBranchPredictor(String name, core_id_t core_id);
   ~StaticBranchPredictor();

   bool predict(IntPtr ip, IntPtr target);
   void update(bool predicted, bool actual, IntPtr ip, IntPtr target);
};

#endif