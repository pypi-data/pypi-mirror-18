/*****************************************************************************
MiniSat -- Copyright (c) 2003-2006, Niklas Een, Niklas Sorensson
CryptoMiniSat -- Copyright (c) 2009 Mate Soos
PyCryptoMS -- Copyright (c) 2011 Michel Le Borgne

Original code by MiniSat authors are under an MIT licence.
Modifications for CryptoMiniSat are under GPLv3 licence.
Modification for PyCryptoMS  are under GPLv3 licence.
******************************************************************************/

#ifndef CRYPTOMS_H
#define CRYPTOMS_H

#include <string>
using std::string;
#include <vector>
//#ifndef DISABLE_ZLIB
//#include <zlib.h>
//#endif // DISABLE_ZLIB

#include "Solver.h"

class CryptoMS
{
 public:
  CryptoMS();
  CryptoMS(std::vector<std::string> options);
  ~CryptoMS(void);

  // management and statistiss
  void set_options(std::vector<std::string> options);
  void clear_solver();
  void print_stats(); // for debug
  void print_nb_clauses_vars(); // for debug
  int nb_clauses();
  int nb_vars();

  // clauses loading
  bool add_clause(std::vector<int> dim);
  void read_in_a_file(const std::string& filename);

  // problem solving
  const std::vector<int>  solve(void);
  const std::vector<std::vector<int> > msolve(int max_nb_sol);
  const std::vector<std::vector<int> > msolve_selected(int max_nr_of_solutions, std::vector<int> var_selected);
  bool is_satisfiable();

  
 private:
  const char* has_prefix(const char*, const char* prefix);
  void acc_models(const CMSat::lbool ret);

  void set_double_precision(const uint32_t verbosity);
  int correct_return_value(const CMSat::lbool ret) const;

  CMSat::SolverConf conf;
  CMSat::GaussConf gaussconfig;
  CMSat::Solver *solver;

  std::vector<std::vector<int> > solutions;
};

//class for exceptions
class CryptoMSError{
 public:
  std::string message;
  
  CryptoMSError();
  CryptoMSError(char* _message);
  CryptoMSError(std::string _message);
}; 


#endif //CRYPTOMS_H
