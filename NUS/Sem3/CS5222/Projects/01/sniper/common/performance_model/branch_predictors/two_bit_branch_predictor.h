#ifndef TWO_BIT_BRANCH_PREDICTOR_H
#define TWO_BIT_BRANCH_PREDICTOR_H

#include "branch_predictor.h"

#include <vector>

class TwoBitBranchPredictor : public BranchPredictor
{
public:
   TwoBitBranchPredictor(String name, core_id_t core_id, UInt32 size);
   ~TwoBitBranchPredictor();

   bool predict(IntPtr ip, IntPtr target);
   void update(bool predicted, bool actual, IntPtr ip, IntPtr target);

private:
   std::vector<int> m_bits;
   static bool get_from_state(int value)
   {
      switch(value)
      {
         case 2:
         case 3:
         return true;
         case 0:
         case 1:
         default:
         return false;
      }
   }
   static int update_state(int value, bool result)
   {
      if (result)
      {
         value++;
         if (value > 3) value = 3;
      }
      else
      {
         value--;
         if (value < 0) value = 0;
      }
      return value;
   }
};

#endif
