%module pyCryptoMS 
%include "typemaps.i"
%include "std_string.i"
%include "exception.i"
%include "std_vector.i"


%{
#include "CryptoMS.h"
%}

// Instantiate templates used by example
namespace std {
   %template(IntVector) vector<int>;
   %template(IntVectorVector) vector<vector<int> >;
   %template(StringVector)vector<string>;
}


%exception  {
  try {
	$function;
      }
  catch (CryptoMSError e)
  {
        PyErr_SetString(PyExc_Exception, e.message.c_str());
	return NULL;
  }
}


class CryptoMS
{
 public:
  CryptoMS();
  ~CryptoMS(void);

  // management and statistisc
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
  const std::vector<int> solve(void);
  const std::vector<std::vector<int> > msolve(int max_nb_sol);
  const std::vector<std::vector<int> > msolve_selected(int max_nr_of_solutions, std::vector<int> var_selected);	
  bool is_satisfiable();
};


class CryptoMSError{
 public:
  std::string message;
  
  CryptoMSError();
  CryptoMSError(char* _message);
  CryptoMSError(std::string _message);
}; 
