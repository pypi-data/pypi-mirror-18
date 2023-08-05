/*****************************************************************************
MiniSat -- Copyright (c) 2003-2006, Niklas Een, Niklas Sorensson
CryptoMiniSat -- Copyright (c) 2009 Mate Soos
PyCryptoMS -- Copyright (c) 2011 Michel Le Borgne

Original code by MiniSat authors are under an MIT licence.
Modifications for CryptoMiniSat are under GPLv3 licence.
Modifications for PyCryptoMS  are under GPLv3 licence.
******************************************************************************/

/**


*/

#include <ctime>
#include <cstring>
#include <errno.h>
#include <string.h>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <omp.h>
#include <stdint.h>
#include <map>
#include <set>
#include <algorithm>

#include <signal.h>


#include "time_mem.h"
#include "constants.h"
#include "DimacsParser.h"

#if defined(__linux__)
#include <fpu_control.h>
#endif

#include "CryptoMS.h"

using namespace CMSat;

CryptoMS::CryptoMS():
  conf(),
  gaussconfig()
{
  solver = new Solver(conf, gaussconfig);
}

CryptoMS::~CryptoMS(){
  delete solver; 
}

void CryptoMS::clear_solver()
{
  delete solver;
  solver = new Solver(conf, gaussconfig);
}

// stats for debug
void CryptoMS::print_stats()
{
  solver->printStats();
}

// config
void CryptoMS::print_nb_clauses_vars()
{
  printf("NB Clauses: %i\n",solver->nClauses());
  printf("NB Vars: %i\n", solver->nVars());
}

int CryptoMS::nb_clauses()
{
  return solver->nClauses();
}

int CryptoMS::nb_vars()
{
  return solver->nVars();
}

const char* CryptoMS::has_prefix(const char* str, const char* prefix)
{
  int len = strlen(prefix);
  if (strncmp(str, prefix, len) == 0)
    return str + len;
  else
    return NULL;
}

void CryptoMS::set_options(std::vector<std::string> options)
{
  const char* value;
  char tmpFilename[201], mess[100];
  tmpFilename[0] = '\0';
  char *cstr;

  conf.verbosity = 0; // chut

  for (uint32_t i = 0; i < options.size(); i++) {
    cstr = new char [options[i].size()+1];
    strcpy (cstr, options[i].c_str());

    if ((value = has_prefix(cstr, "polarity-mode="))) {
      if (strcmp(value, "true") == 0)
	conf.polarity_mode = polarity_true;
      else if (strcmp(value, "false") == 0)
	conf.polarity_mode = polarity_false;
      else if (strcmp(value, "rnd") == 0)
	conf.polarity_mode = polarity_rnd;
      else if (strcmp(value, "auto") == 0)
	conf.polarity_mode = polarity_auto;
      else {
	sprintf(mess,"ERROR! unknown polarity-mode %s\n", value);
	throw CryptoMSError(mess);
      }

    } else if ((value = has_prefix(cstr, "rnd-freq="))) {
      double rnd;
      if (sscanf(value, "%lf", &rnd) <= 0 || rnd < 0 || rnd > 1) {
	sprintf(mess, "ERROR! illegal rnRSE ERROR!d-freq constant %s\n", value);
	throw CryptoMSError(mess);
      }
      conf.random_var_freq = rnd;

    } else if ((value = has_prefix(cstr, "verbosity="))) {
      int verbosity = (int)strtol(value, NULL, 10);
      if (verbosity == EINVAL || verbosity == ERANGE) {
	sprintf(mess, "ERROR! illegal verbosity level %s\n", value);
	throw CryptoMSError(mess);
      }
      conf.verbosity = verbosity;

#ifdef STATS_NEEDED
    } else if ((value = has_prefix(cstr, "proof-log"))) {
      conf.needProofGraph();

    } else if ((value = has_prefix(cstr, "stats"))) {
      conf.needStats();
#endif

    } else if ((value = has_prefix(cstr, "randomize="))) {
      uint32_t seed;
      if (sscanf(value, "%d", &seed) < 0) {
	sprintf(mess, "ERROR! illegal seed %s\n", value);
	throw CryptoMSError(mess);
      }
      conf.origSeed = seed;

    } else if ((value = has_prefix(cstr, "restrict="))) {
      uint32_t branchTo;
      if (sscanf(value, "%d", &branchTo) < 0 || branchTo < 1) {
	sprintf(mess, "ERROR! illegal restricted pick branch number %d\n", branchTo);
	throw CryptoMSError(mess);
      }
      conf.restrictPickBranch = branchTo;

    } else if ((value = has_prefix(cstr, "gaussuntil="))) {
      uint32_t until;
      if (sscanf(value, "%d", &until) < 0) {
	sprintf(mess, "ERROR! until %s\n", value);
	throw CryptoMSError(mess);
      }
      gaussconfig.decision_until = until;

    } else if ((value = has_prefix(cstr, "restarts="))) {
      uint32_t maxrest;
      if (sscanf(value, "%d", &maxrest) < 0 || maxrest == 0) {
	sprintf(mess, "ERROR! illegal maximum restart number %d\n", maxrest);
	throw CryptoMSError(mess);
      }
      conf.maxRestarts = maxrest;

    } else if ((value = has_prefix(cstr, "dumplearnts="))) {
      if (sscanf(value, "%200s", tmpFilename) < 0 || strlen(tmpFilename) == 0) {
	sprintf(mess, "ERROR! wrong filename '%s'\n", tmpFilename);
	throw CryptoMSError(mess);
      }
      conf.learntsFilename.assign(tmpFilename);
      conf.needToDumpLearnts = true;

    } else if ((value = has_prefix(cstr, "dumporig="))) {
      if (sscanf(value, "%200s", tmpFilename) < 0 || strlen(tmpFilename) == 0) {
	sprintf(mess, "ERROR! wrong filename '%s'\n", tmpFilename);
	throw CryptoMSError(mess);
      }
      conf.origFilename.assign(tmpFilename);
      conf.needToDumpOrig = true;

    } else if ((value = has_prefix(cstr, "maxdumplearnts="))) {
      if (!conf.needToDumpLearnts) {
	sprintf(mess, "ERROR! -dumplearnts=<filename> must be first activated before issuing -maxdumplearnts=<size>\n");
	throw CryptoMSError(mess);
      }
      int tmp;
      if (sscanf(value, "%d", &tmp) < 0 || tmp < 0) {
	sprintf(mess, "ERROR! wrong maximum dumped learnt clause size is illegal:%i\n",tmp);
	throw CryptoMSError(mess);
      }
      conf.maxDumpLearntsSize = (uint32_t)tmp;

    } else if ((value = has_prefix(cstr, "pavgbranch"))) {
      conf.doPrintAvgBranch = true;

    } else if ((value = has_prefix(cstr, "greedyunbound"))) {
      conf.greedyUnbound = true;

    } else if ((value = has_prefix(cstr, "nonormxorfind"))) {
      conf.doFindXors = false;

    } else if ((value = has_prefix(cstr, "nobinxorfind"))) {
      conf.doFindEqLits = false;

    } else if ((value = has_prefix(cstr, "noregbxorfind"))) {
      conf.doRegFindEqLits = false;

    } else if ((value = has_prefix(cstr, "noextendedscc"))) {
      conf.doExtendedSCC = false;

    } else if ((value = has_prefix(cstr, "noconglomerate"))) {
      conf.doConglXors = false;

    } else if ((value = has_prefix(cstr, "nosimplify"))) {
      conf.doSchedSimp = false;

    } else if ((value = has_prefix(cstr, "novarreplace"))) {
      conf.doReplace = false;

    } else if ((value = has_prefix(cstr, "nofailedlit"))) {
      conf.doFailedLit = false;

    } else if ((value = has_prefix(cstr, "nodisablegauss"))) {
      gaussconfig.dontDisable = true;

    } else if ((value = has_prefix(cstr, "maxnummatrixes="))) {
      uint32_t maxNumMatrixes;
      if (sscanf(value, "%d", &maxNumMatrixes) < 0) {
	sprintf(mess, "ERROR! maxnummatrixes: %s\n", value);
	throw CryptoMSError(mess);
      }
      gaussconfig.maxNumMatrixes = maxNumMatrixes;

    } else if ((value = has_prefix(cstr, "noheuleprocess"))) {
      conf.doHeuleProcess = false;

    } else if ((value = has_prefix(cstr, "nosatelite"))) {
      conf.doSatELite = false;

    // } else if ((value = has_prefix(cstr, "noparthandler"))) {
    //   conf.doPartHandler = false;

    } else if ((value = has_prefix(cstr, "noxorsubs"))) {
      conf.doXorSubsumption = false;

    } else if ((value = has_prefix(cstr, "nohyperbinres"))) {
      conf.doHyperBinRes = false;

    } else if ((value = has_prefix(cstr, "novarelim"))) {
      conf.doVarElim = false;

    } else if ((value = has_prefix(cstr, "nosubsume1"))) {
      conf.doSubsume1 = false;

    } else if ((value = has_prefix(cstr, "nomatrixfind"))) {
      gaussconfig.noMatrixFind = true;

    } else if ((value = has_prefix(cstr, "noiterreduce"))) {
      gaussconfig.iterativeReduce = false;

    } else if ((value = has_prefix(cstr, "noiterreduce"))) {
      gaussconfig.iterativeReduce = false;

    } else if ((value = has_prefix(cstr, "noordercol"))) {
      gaussconfig.orderCols = false;

    } else if ((value = has_prefix(cstr, "maxmatrixrows="))) {
      int rows;
      if (sscanf(value, "%d", &rows) < 0 || rows < 0) {
	sprintf(mess, "ERROR! maxmatrixrows: %s\n", value);
	throw CryptoMSError(mess);
      }
      gaussconfig.maxMatrixRows = (uint32_t)rows;

    } else if ((value = has_prefix(cstr, "minmatrixrows="))) {
      int rows;
      if (sscanf(value, "%d", &rows) < 0 || rows < 0) {
	sprintf(mess, "ERROR! minmatrixrows: %s\n", value);
	throw CryptoMSError(mess);
      }
      gaussconfig.minMatrixRows = rows;

    } else if ((value = has_prefix(cstr, "savematrix"))) {
      uint32_t every;
      if (sscanf(value, "%d", &every) < 0) {
	sprintf(mess, "ERROR! savematrix: %s\n", value);
	throw CryptoMSError(mess);
      }
      gaussconfig.only_nth_gauss_save = every;
       
    } else if ((value = has_prefix(cstr, "restart="))) {
      if (strcmp(value, "auto") == 0)
	conf.fixRestartType = auto_restart;
      else if (strcmp(value, "static") == 0)
	conf.fixRestartType = static_restart;
      else if (strcmp(value, "dynamic") == 0)
	conf.fixRestartType = dynamic_restart;
      else {
	sprintf(mess, "ERROR! unknown restart type %s\n", value);
	throw CryptoMSError(mess);
      }

    } else if ((value = has_prefix(cstr, "nohyperbinres"))) {
      conf.doHyperBinRes= false;

    } else if ((value = has_prefix(cstr, "noremovebins"))) {
      conf.doRemUselessBins = false;

    } else if ((value = has_prefix(cstr, "nosubswithnbins"))) {
      conf.doSubsWNonExistBins = false;

    } else if ((value = has_prefix(cstr, "nosubswithbins"))) {
      conf.doSubsWBins = false;

    } else if ((value = has_prefix(cstr, "noclausevivif"))) {
      conf.doClausVivif = false;

    } else if ((value = has_prefix(cstr, "nosortwatched"))) {
      conf.doSortWatched = false;

    } else if ((value = has_prefix(cstr, "nolfminim"))) {
      conf.doMinimLearntMore = false;

    } else if ((value = has_prefix(cstr, "nocalcreach"))) {
      conf.doCalcReach = false;

    } else if ((value = has_prefix(cstr, "norecotfssr"))) {
      conf.doMinimLMoreRecur = false;

    } else if ((value = has_prefix(cstr, "nocacheotfssr"))) {
      conf.doCacheOTFSSR = false;

    } else if ((value = has_prefix(cstr, "noremlbins"))) {
      conf.doRemUselessLBins = false;

    // } else if ((value = has_prefix(cstr, "maxglue="))) {
    //   int glue = 0;
    //   if (sscanf(value, "%d", &glue) < 0 || glue < 2) {
    // 	sprintf(mess, "ERROR! maxGlue: %s\n", value);
    // 	throw CryptoMSError(mess);
    //   }
    //   if (glue >= (1<< MAX_GLUE_BITS)-1) {
    // 	sprintf(mess, "Due to memory-packing limitations, max glue cannot be more than %i\n", 
    // 		((1<< MAX_GLUE_BITS)-2));
    // 	throw CryptoMSError(mess);
    //   }
    //   conf.maxGlue = (uint32_t)glue;
    // } else if ((value = has_prefix(cstr, "maxgluedel"))) {
    //   conf.doMaxGlueDel = true;

      //         } else if ((value = has_prefix(cstr, "threads="))) {
      //             numThreads = 0;
      //             if (sscanf(value, "%d", &numThreads) < 0 || numThreads < 1) {
      // 	      sprintf(mess, "ERROR! numThreads: %s\n", value);
      //               throw CryptoMSError(mess);
      //             }

    } else {
      sprintf(mess,"ERROR! unknown option %s\n", cstr);
      throw CryptoMSError(mess);
    }
    delete[] cstr; 	
  }// END for
}// END set_options


bool CryptoMS::add_clause(std::vector<int> dimacs)
{
  int il;
  uint32_t i,var;
  vec<Lit> lits;
  if (dimacs.size() == 0) return false;
  lits.clear();
  for (i=0; i<dimacs.size(); i++) 
    {
      il = dimacs[i];
      if (il == 0) {
	std::string mess("Incorrect dimacs format in clause");
	throw CryptoMSError(mess);
      }
      var = abs(il)-1;
      while (var >= solver->nVars()) solver->newVar();
      lits.push( (il > 0) ? Lit(var, false) : Lit(var, true) );
    }
  return solver->addClause(lits);
}


void CryptoMS::read_in_a_file(const std::string& filename)
{
  char* fname = (char*)calloc(filename.length()+1, sizeof(char));
  char mess[70];
  assert(fname != NULL);
  memcpy(fname, filename.c_str(), filename.length());
  fname[filename.length()] = '\0';
#ifdef DISABLE_ZLIB
  FILE * in = fopen(fname, "rb");
#else
  gzFile in = gzopen(fname, "rb");
#endif // DISABLE_ZLIB
  free(fname);
  
  if (in == NULL) {
    sprintf(mess, "ERROR! Could not open file %s for reading \n", filename.c_str());
    throw CryptoMSError(mess);
  }
  
  DimacsParser parser(solver, false, false, false);
  parser.parse_DIMACS(in);
  
#ifdef DISABLE_ZLIB
  fclose(in);
#else
  gzclose(in);
#endif // DISABLE_ZLIB
}



void CryptoMS::set_double_precision(const uint32_t verbosity)
{
#if defined(__linux__)
  fpu_control_t oldcw, newcw;
  _FPU_GETCW(oldcw);
  newcw = (oldcw & ~_FPU_EXTENDED) | _FPU_DOUBLE;
  _FPU_SETCW(newcw);
  if (verbosity >= 1) printf("c WARNING: for repeatability, setting FPU to use double precision\n");
#endif
}


void CryptoMS::acc_models(const lbool ret)
{
  int sign;
  vector<int> sol;
  if (ret == l_True)
    {
      for (Var var = 0; var != solver->nVars(); var++)
	if (solver->model[var] != l_Undef)
	  {
	    (solver->model[var] == l_True)? sign=1 : sign=-1;
	    sol.push_back((var+1)*sign);
	  }
      solutions.push_back(sol);
    }
}


const std::vector<int>  CryptoMS::solve(void)
{
  lbool ret = l_True;
  std::vector<int> sol;
  int sign;
 
  set_double_precision(conf.verbosity);
  sol.clear();
  ret = solver->solve();
  if (ret == l_True)
    {
      for (Var var = 0; var != solver->nVars(); var++)
	if (solver->model[var] != l_Undef)
	  {
	    (solver->model[var] == l_True)? sign=1 : sign=-1;
	    sol.push_back((var+1)*sign);
	  }
    }
  return sol;
}

const std::vector<std::vector<int> > CryptoMS::msolve(int max_nr_of_solutions)
{
  int current_nr_of_solutions = 0;
  lbool ret = l_True;

  set_double_precision(conf.verbosity);
  solutions.clear();

  while(current_nr_of_solutions < max_nr_of_solutions && ret == l_True) {
    ret = solver->solve();
    current_nr_of_solutions++;

    if (ret == l_True && current_nr_of_solutions < max_nr_of_solutions) {
      if (conf.verbosity >= 1) std::cout << "c Prepare for next run..." << std::endl;

      acc_models(ret);
      vec<Lit> lits;
      for (Var var = 0; var != solver->nVars(); var++) {
	if (solver->model[var] != l_Undef) {
	  lits.push( Lit(var, (solver->model[var] == l_True)? true : false) );
	}
      }
      solver->addClause(lits);
    }
  }
  acc_models(ret);
  return solutions;
}


const std::vector<std::vector<int> > CryptoMS::msolve_selected(int max_nr_of_solutions, 
							     std::vector<int> var_selected)
{
  int current_nr_of_solutions = 0;
  lbool ret = l_True;
  vector<int>::iterator p;


  set_double_precision(conf.verbosity);
  solutions.clear();
  std::sort( var_selected.begin(), var_selected.end() );

  while(current_nr_of_solutions < max_nr_of_solutions && ret == l_True) {
    ret = solver->solve();
    current_nr_of_solutions++;

    if (ret == l_True && current_nr_of_solutions < max_nr_of_solutions) {
      if (conf.verbosity >= 1) std::cout << "c Prepare for next run..." << std::endl;

      acc_models(ret);
      vec<Lit> lits;
      for (Var var = 0; var != solver->nVars(); var++) 
	{
	  p = std::find(var_selected.begin(), var_selected.end(), var+1);
	  if (solver->model[var] != l_Undef && p!=var_selected.end())
	      lits.push( Lit(var, (solver->model[var] == l_True)? true : false) );
	}
      solver->addClause(lits);
    }
  }
  acc_models(ret);
  return solutions;
}

bool  CryptoMS::is_satisfiable()
{
  lbool ret;

  set_double_precision(conf.verbosity);
  ret = solver->solve();
  return (ret == l_True);
}



// Exceptions
CryptoMSError::CryptoMSError(): message(""){};
CryptoMSError::CryptoMSError(char* _message): message(_message) {};
CryptoMSError::CryptoMSError(std::string _message): message(_message) {};
