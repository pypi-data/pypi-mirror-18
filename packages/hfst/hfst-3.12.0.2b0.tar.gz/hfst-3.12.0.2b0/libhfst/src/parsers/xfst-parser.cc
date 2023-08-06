/* A Bison parser, made by GNU Bison 2.5.  */

/* Bison implementation for Yacc-like parsers in C
   
      Copyright (C) 1984, 1989-1990, 2000-2011 Free Software Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "2.5"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1

/* Using locations.  */
#define YYLSP_NEEDED 1

/* Substitute the variable and function names.  */
#define yyparse         hxfstparse
#define yylex           hxfstlex
#define yyerror         hxfsterror
#define yylval          hxfstlval
#define yychar          hxfstchar
#define yydebug         hxfstdebug
#define yynerrs         hxfstnerrs
#define yylloc          hxfstlloc

/* Copy the first part of user declarations.  */

/* Line 268 of yacc.c  */
#line 1 "xfst-parser.yy"

// Copyright (c) 2016 University of Helsinki
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 3 of the License, or (at your option) any later version.
// See the file COPYING included with this distribution for more
// information.

//! @file xfst-parser.yy
//!
//! @brief A parser for xfst
//!
//! @author Tommi A. Pirinen

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <cstdlib>
#include <cstdio>

#include <string>
using std::string;

namespace hfst {
  class HfstTransducer;
}

#include "XfstCompiler.h"
#include "xfst-utils.h"

#define CHECK if (hfst::xfst::xfst_->get_fail_flag()) { YYABORT; }

// obligatory yacc stuff
extern int hxfstlineno;
void hxfsterror(const char *text);
int hxfstlex(void);



/* Line 268 of yacc.c  */
#line 122 "xfst-parser.cc"

/* Enabling traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 1
#endif

/* Enabling the token table.  */
#ifndef YYTOKEN_TABLE
# define YYTOKEN_TABLE 0
#endif


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     APROPOS = 258,
     DESCRIBE = 259,
     ECHO = 260,
     SYSTEM = 261,
     QUIT = 262,
     HFST = 263,
     NAMETOKEN = 264,
     NAMECHAR = 265,
     GLOB = 266,
     PROTOTYPE = 267,
     DEFINE_NAME = 268,
     DEFINE_FUNCTION = 269,
     RANGE = 270,
     REDIRECT_IN = 271,
     REDIRECT_OUT = 272,
     SAVE_PROLOG = 273,
     FOR = 274,
     REVERSE = 275,
     VIEW = 276,
     LOADD = 277,
     PRINT_LABEL_COUNT = 278,
     TEST_OVERLAP = 279,
     TEST_NONNULL = 280,
     CONCATENATE = 281,
     LOADS = 282,
     INVERT = 283,
     PRINT_ALIASES = 284,
     PRINT_LABELS = 285,
     XFST_OPTIONAL = 286,
     PRINT_SHORTEST_STRING_SIZE = 287,
     READ_PROPS = 288,
     TEST_FUNCT = 289,
     PRINT_LABELMAPS = 290,
     SUBSTRING = 291,
     COMPOSE = 292,
     READ_SPACED = 293,
     TEST_UPPER_UNI = 294,
     COLLECT_EPSILON_LOOPS = 295,
     ZERO_PLUS = 296,
     INSPECT = 297,
     ROTATE = 298,
     PRINT_WORDS = 299,
     POP = 300,
     SAVE_SPACED = 301,
     DEFINE = 302,
     SHOW = 303,
     PRINT_LONGEST_STRING_SIZE = 304,
     TEST_EQ = 305,
     SORT = 306,
     SAVE_DEFINITIONS = 307,
     SAVE_DOT = 308,
     TEST_UPPER_BOUNDED = 309,
     COMPLETE = 310,
     PRINT_FILE_INFO = 311,
     INTERSECT = 312,
     END_SUB = 313,
     TURN = 314,
     PRINT_LIST = 315,
     SUBSTITUTE_SYMBOL = 316,
     APPLY_UP = 317,
     ONE_PLUS = 318,
     UNDEFINE = 319,
     EPSILON_REMOVE = 320,
     PRINT_RANDOM_WORDS = 321,
     CTRLD = 322,
     EXTRACT_UNAMBIGUOUS = 323,
     SEMICOLON = 324,
     PRINT_LOWER_WORDS = 325,
     READ_PROLOG = 326,
     CLEAR = 327,
     PRINT_SIGMA_COUNT = 328,
     SUBSTITUTE_NAMED = 329,
     PRINT_FLAGS = 330,
     SET = 331,
     NEGATE = 332,
     APPLY_DOWN = 333,
     PRINT_STACK = 334,
     SAVE_STACK = 335,
     PUSH = 336,
     TEST_LOWER_BOUNDED = 337,
     PRINT_DEFINED = 338,
     APPLY_MED = 339,
     SHOW_ALL = 340,
     PRINT_ARCCOUNT = 341,
     PRINT_SIZE = 342,
     TEST_NULL = 343,
     PRINT_RANDOM_UPPER = 344,
     PRINT_LONGEST_STRING = 345,
     UPPER_SIDE = 346,
     XFST_IGNORE = 347,
     TEST_UNAMBIGUOUS = 348,
     PRINT = 349,
     READ_TEXT = 350,
     UNLIST = 351,
     SUBSTITUTE_LABEL = 352,
     SAVE_DEFINITION = 353,
     ELIMINATE_FLAG = 354,
     EDIT_PROPS = 355,
     PRINT_UPPER_WORDS = 356,
     NAME = 357,
     EXTRACT_AMBIGUOUS = 358,
     DEFINE_ALIAS = 359,
     PRINT_RANDOM_LOWER = 360,
     CROSSPRODUCT = 361,
     COMPACT_SIGMA = 362,
     SOURCE = 363,
     AMBIGUOUS = 364,
     ELIMINATE_ALL = 365,
     PRINT_SIGMA = 366,
     PRINT_SHORTEST_STRING = 367,
     LEFT_PAREN = 368,
     PRINT_PROPS = 369,
     READ_REGEX = 370,
     DEFINE_LIST = 371,
     TEST_ID = 372,
     PRINT_LISTS = 373,
     TEST_SUBLANGUAGE = 374,
     TEST_LOWER_UNI = 375,
     COMPILE_REPLACE_UPPER = 376,
     CLEANUP = 377,
     ADD_PROPS = 378,
     PRINT_SIGMA_WORD_COUNT = 379,
     SHUFFLE = 380,
     COLON = 381,
     SAVE_TEXT = 382,
     DETERMINIZE = 383,
     SIGMA = 384,
     COMPILE_REPLACE_LOWER = 385,
     UNION = 386,
     PRINT_DIR = 387,
     LIST = 388,
     LOWER_SIDE = 389,
     MINIMIZE = 390,
     MINUS = 391,
     PRINT_NAME = 392,
     PRUNE_NET = 393,
     PUSH_DEFINED = 394,
     READ_LEXC = 395,
     READ_ATT = 396,
     TWOSIDED_FLAGS = 397,
     WRITE_ATT = 398,
     ASSERT = 399,
     LABEL_NET = 400,
     LOOKUP_OPTIMIZE = 401,
     REMOVE_OPTIMIZATION = 402,
     TEST_INFINITELY_AMBIGUOUS = 403,
     XFST_ERROR = 404,
     NEWLINE = 405,
     REGEX = 406,
     APPLY_INPUT = 407
   };
#endif
/* Tokens.  */
#define APROPOS 258
#define DESCRIBE 259
#define ECHO 260
#define SYSTEM 261
#define QUIT 262
#define HFST 263
#define NAMETOKEN 264
#define NAMECHAR 265
#define GLOB 266
#define PROTOTYPE 267
#define DEFINE_NAME 268
#define DEFINE_FUNCTION 269
#define RANGE 270
#define REDIRECT_IN 271
#define REDIRECT_OUT 272
#define SAVE_PROLOG 273
#define FOR 274
#define REVERSE 275
#define VIEW 276
#define LOADD 277
#define PRINT_LABEL_COUNT 278
#define TEST_OVERLAP 279
#define TEST_NONNULL 280
#define CONCATENATE 281
#define LOADS 282
#define INVERT 283
#define PRINT_ALIASES 284
#define PRINT_LABELS 285
#define XFST_OPTIONAL 286
#define PRINT_SHORTEST_STRING_SIZE 287
#define READ_PROPS 288
#define TEST_FUNCT 289
#define PRINT_LABELMAPS 290
#define SUBSTRING 291
#define COMPOSE 292
#define READ_SPACED 293
#define TEST_UPPER_UNI 294
#define COLLECT_EPSILON_LOOPS 295
#define ZERO_PLUS 296
#define INSPECT 297
#define ROTATE 298
#define PRINT_WORDS 299
#define POP 300
#define SAVE_SPACED 301
#define DEFINE 302
#define SHOW 303
#define PRINT_LONGEST_STRING_SIZE 304
#define TEST_EQ 305
#define SORT 306
#define SAVE_DEFINITIONS 307
#define SAVE_DOT 308
#define TEST_UPPER_BOUNDED 309
#define COMPLETE 310
#define PRINT_FILE_INFO 311
#define INTERSECT 312
#define END_SUB 313
#define TURN 314
#define PRINT_LIST 315
#define SUBSTITUTE_SYMBOL 316
#define APPLY_UP 317
#define ONE_PLUS 318
#define UNDEFINE 319
#define EPSILON_REMOVE 320
#define PRINT_RANDOM_WORDS 321
#define CTRLD 322
#define EXTRACT_UNAMBIGUOUS 323
#define SEMICOLON 324
#define PRINT_LOWER_WORDS 325
#define READ_PROLOG 326
#define CLEAR 327
#define PRINT_SIGMA_COUNT 328
#define SUBSTITUTE_NAMED 329
#define PRINT_FLAGS 330
#define SET 331
#define NEGATE 332
#define APPLY_DOWN 333
#define PRINT_STACK 334
#define SAVE_STACK 335
#define PUSH 336
#define TEST_LOWER_BOUNDED 337
#define PRINT_DEFINED 338
#define APPLY_MED 339
#define SHOW_ALL 340
#define PRINT_ARCCOUNT 341
#define PRINT_SIZE 342
#define TEST_NULL 343
#define PRINT_RANDOM_UPPER 344
#define PRINT_LONGEST_STRING 345
#define UPPER_SIDE 346
#define XFST_IGNORE 347
#define TEST_UNAMBIGUOUS 348
#define PRINT 349
#define READ_TEXT 350
#define UNLIST 351
#define SUBSTITUTE_LABEL 352
#define SAVE_DEFINITION 353
#define ELIMINATE_FLAG 354
#define EDIT_PROPS 355
#define PRINT_UPPER_WORDS 356
#define NAME 357
#define EXTRACT_AMBIGUOUS 358
#define DEFINE_ALIAS 359
#define PRINT_RANDOM_LOWER 360
#define CROSSPRODUCT 361
#define COMPACT_SIGMA 362
#define SOURCE 363
#define AMBIGUOUS 364
#define ELIMINATE_ALL 365
#define PRINT_SIGMA 366
#define PRINT_SHORTEST_STRING 367
#define LEFT_PAREN 368
#define PRINT_PROPS 369
#define READ_REGEX 370
#define DEFINE_LIST 371
#define TEST_ID 372
#define PRINT_LISTS 373
#define TEST_SUBLANGUAGE 374
#define TEST_LOWER_UNI 375
#define COMPILE_REPLACE_UPPER 376
#define CLEANUP 377
#define ADD_PROPS 378
#define PRINT_SIGMA_WORD_COUNT 379
#define SHUFFLE 380
#define COLON 381
#define SAVE_TEXT 382
#define DETERMINIZE 383
#define SIGMA 384
#define COMPILE_REPLACE_LOWER 385
#define UNION 386
#define PRINT_DIR 387
#define LIST 388
#define LOWER_SIDE 389
#define MINIMIZE 390
#define MINUS 391
#define PRINT_NAME 392
#define PRUNE_NET 393
#define PUSH_DEFINED 394
#define READ_LEXC 395
#define READ_ATT 396
#define TWOSIDED_FLAGS 397
#define WRITE_ATT 398
#define ASSERT 399
#define LABEL_NET 400
#define LOOKUP_OPTIMIZE 401
#define REMOVE_OPTIMIZATION 402
#define TEST_INFINITELY_AMBIGUOUS 403
#define XFST_ERROR 404
#define NEWLINE 405
#define REGEX 406
#define APPLY_INPUT 407




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 293 of yacc.c  */
#line 51 "xfst-parser.yy"

    char* name;
    char* text;
    char** list;
    char* file;
    void* nothing;



/* Line 293 of yacc.c  */
#line 472 "xfst-parser.cc"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
} YYLTYPE;
# define yyltype YYLTYPE /* obsolescent; will be withdrawn */
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif


/* Copy the second part of user declarations.  */


/* Line 343 of yacc.c  */
#line 497 "xfst-parser.cc"

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#elif (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
typedef signed char yytype_int8;
#else
typedef short int yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(e) ((void) (e))
#else
# define YYUSE(e) /* empty */
#endif

/* Identity function, used to suppress warnings about constant conditions.  */
#ifndef lint
# define YYID(n) (n)
#else
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static int
YYID (int yyi)
#else
static int
YYID (yyi)
    int yyi;
#endif
{
  return yyi;
}
#endif

#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's `empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (YYID (0))
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
	     && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
	 || (defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL \
	     && defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
  YYLTYPE yyls_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE) + sizeof (YYLTYPE)) \
      + 2 * YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)				\
    do									\
      {									\
	YYSIZE_T yynewbytes;						\
	YYCOPY (&yyptr->Stack_alloc, Stack, yysize);			\
	Stack = &yyptr->Stack_alloc;					\
	yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
	yyptr += yynewbytes / sizeof (*yyptr);				\
      }									\
    while (YYID (0))

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from FROM to TO.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(To, From, Count) \
      __builtin_memcpy (To, From, (Count) * sizeof (*(From)))
#  else
#   define YYCOPY(To, From, Count)		\
      do					\
	{					\
	  YYSIZE_T yyi;				\
	  for (yyi = 0; yyi < (Count); yyi++)	\
	    (To)[yyi] = (From)[yyi];		\
	}					\
      while (YYID (0))
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  348
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   918

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  153
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  10
/* YYNRULES -- Number of rules.  */
#define YYNRULES  262
/* YYNRULES -- Number of states.  */
#define YYNSTATES  539

/* YYTRANSLATE(YYLEX) -- Bison symbol number corresponding to YYLEX.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   407

#define YYTRANSLATE(YYX)						\
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[YYLEX] -- Bison symbol number corresponding to YYLEX.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,    99,   100,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,   120,   121,   122,   123,   124,
     125,   126,   127,   128,   129,   130,   131,   132,   133,   134,
     135,   136,   137,   138,   139,   140,   141,   142,   143,   144,
     145,   146,   147,   148,   149,   150,   151,   152
};

#if YYDEBUG
/* YYPRHS[YYN] -- Index of the first RHS symbol of rule number YYN in
   YYRHS.  */
static const yytype_uint16 yyprhs[] =
{
       0,     0,     3,     5,     8,    11,    13,    17,    21,    24,
      27,    31,    35,    39,    44,    47,    51,    55,    59,    64,
      68,    72,    77,    80,    83,    86,    89,    92,    97,   103,
     109,   114,   116,   119,   122,   126,   130,   134,   138,   141,
     144,   147,   150,   154,   157,   160,   163,   167,   171,   176,
     179,   182,   186,   189,   191,   193,   195,   199,   201,   204,
     209,   213,   216,   219,   222,   225,   228,   230,   233,   236,
     239,   242,   245,   248,   251,   254,   257,   261,   265,   269,
     273,   277,   281,   285,   289,   293,   297,   301,   305,   311,
     317,   323,   327,   330,   334,   338,   341,   345,   348,   353,
     357,   361,   364,   368,   371,   375,   378,   382,   386,   389,
     393,   396,   401,   405,   409,   412,   416,   419,   423,   426,
     430,   433,   437,   440,   444,   447,   452,   458,   462,   465,
     470,   474,   479,   485,   489,   492,   497,   501,   506,   512,
     516,   519,   524,   528,   533,   539,   543,   546,   551,   555,
     560,   566,   570,   573,   578,   582,   587,   593,   597,   600,
     605,   609,   613,   617,   620,   624,   627,   631,   635,   639,
     642,   646,   649,   653,   657,   660,   664,   668,   671,   675,
     678,   682,   686,   690,   693,   699,   704,   709,   713,   717,
     720,   724,   728,   732,   735,   739,   742,   746,   749,   753,
     756,   760,   763,   766,   770,   775,   779,   783,   787,   791,
     795,   799,   803,   808,   812,   816,   819,   823,   827,   833,
     836,   839,   842,   845,   848,   851,   854,   857,   860,   863,
     866,   869,   872,   875,   878,   881,   884,   887,   890,   893,
     896,   899,   902,   905,   908,   911,   914,   917,   920,   922,
     925,   927,   928,   931,   934,   936,   939,   941,   944,   946,
     950,   952,   955
};

/* YYRHS -- A `-1'-separated list of the rules' RHS.  */
static const yytype_int16 yyrhs[] =
{
     154,     0,    -1,   155,    -1,   155,    67,    -1,   155,   156,
      -1,   156,    -1,   123,    16,   157,    -1,   123,   159,    67,
      -1,   100,   157,    -1,    62,   157,    -1,    62,   152,   157,
      -1,    62,     9,   157,    -1,    62,    16,   157,    -1,    62,
     157,   159,    58,    -1,    78,   157,    -1,    78,   152,   157,
      -1,    78,     9,   157,    -1,    78,    16,   157,    -1,    78,
     157,   159,    58,    -1,    84,     9,   157,    -1,    84,    16,
     157,    -1,    84,   157,   159,    58,    -1,   146,   157,    -1,
     147,   157,    -1,   109,   157,    -1,   103,   157,    -1,    68,
     157,    -1,   104,     9,   158,   157,    -1,   104,     9,   157,
     159,    58,    -1,   133,     9,   159,    69,   157,    -1,   133,
       9,    15,   157,    -1,    13,    -1,    13,   151,    -1,    14,
     151,    -1,    64,   159,   157,    -1,    96,     9,   157,    -1,
     102,     9,   157,    -1,    22,     9,   157,    -1,     3,   157,
      -1,     4,   157,    -1,    72,   157,    -1,    45,   157,    -1,
     139,     9,   157,    -1,   139,   157,    -1,    59,   157,    -1,
      43,   157,    -1,    27,    16,   157,    -1,    27,     9,   157,
      -1,    27,     9,    69,   157,    -1,    40,   157,    -1,   107,
     157,    -1,    99,     9,   157,    -1,   110,   157,    -1,     5,
      -1,     7,    -1,     8,    -1,   108,     9,   157,    -1,     6,
      -1,    21,   157,    -1,    76,     9,     9,   157,    -1,    48,
       9,   157,    -1,    85,   157,    -1,   142,   157,    -1,    50,
     157,    -1,    34,   157,    -1,   117,   157,    -1,   148,    -1,
      82,   157,    -1,   120,   157,    -1,    54,   157,    -1,    39,
     157,    -1,    25,   157,    -1,    88,   157,    -1,    24,   157,
      -1,   119,   157,    -1,    93,   157,    -1,   144,    50,   157,
      -1,   144,    34,   157,    -1,   144,   117,   157,    -1,   144,
      82,   157,    -1,   144,   120,   157,    -1,   144,    54,   157,
      -1,   144,    39,   157,    -1,   144,    25,   157,    -1,   144,
      88,   157,    -1,   144,    24,   157,    -1,   144,   119,   157,
      -1,   144,    93,   157,    -1,    74,     9,    19,     9,   157,
      -1,    97,   162,    19,   161,   157,    -1,    61,   160,    19,
       9,   157,    -1,    29,    17,   157,    -1,    29,   157,    -1,
      86,    17,   157,    -1,    86,     9,   157,    -1,    86,   157,
      -1,    83,    17,   157,    -1,    83,   157,    -1,   132,    11,
      17,   157,    -1,   132,    11,   157,    -1,   132,    17,   157,
      -1,   132,   157,    -1,    56,    17,   157,    -1,    56,   157,
      -1,    75,    17,   157,    -1,    75,   157,    -1,    30,     9,
     157,    -1,    30,    17,   157,    -1,    30,   157,    -1,    23,
      17,   157,    -1,    23,   157,    -1,    60,     9,    17,   157,
      -1,    60,     9,   157,    -1,   118,    17,   157,    -1,   118,
     157,    -1,    90,    17,   157,    -1,    90,   157,    -1,    49,
      17,   157,    -1,    49,   157,    -1,   137,    17,   157,    -1,
     137,   157,    -1,   112,    17,   157,    -1,   112,   157,    -1,
      32,    17,   157,    -1,    32,   157,    -1,    70,     9,     9,
     157,    -1,    70,     9,     9,    17,   157,    -1,    70,     9,
     157,    -1,    70,   157,    -1,    70,     9,    17,   157,    -1,
      70,    17,   157,    -1,   105,     9,     9,   157,    -1,   105,
       9,     9,    17,   157,    -1,   105,     9,   157,    -1,   105,
     157,    -1,   105,     9,    17,   157,    -1,   105,    17,   157,
      -1,   101,     9,     9,   157,    -1,   101,     9,     9,    17,
     157,    -1,   101,     9,   157,    -1,   101,   157,    -1,   101,
       9,    17,   157,    -1,   101,    17,   157,    -1,    89,     9,
       9,   157,    -1,    89,     9,     9,    17,   157,    -1,    89,
       9,   157,    -1,    89,   157,    -1,    89,     9,    17,   157,
      -1,    89,    17,   157,    -1,    44,     9,     9,   157,    -1,
      44,     9,     9,    17,   157,    -1,    44,     9,   157,    -1,
      44,   157,    -1,    44,     9,    17,   157,    -1,    44,    17,
     157,    -1,    66,     9,     9,   157,    -1,    66,     9,     9,
      17,   157,    -1,    66,     9,   157,    -1,    66,   157,    -1,
      66,     9,    17,   157,    -1,    66,    17,   157,    -1,    94,
       9,   157,    -1,    94,    17,   157,    -1,    94,   157,    -1,
     114,     9,   157,    -1,   114,   157,    -1,   114,    17,   157,
      -1,   111,     9,   157,    -1,   111,    17,   157,    -1,   111,
     157,    -1,    73,    17,   157,    -1,    73,   157,    -1,   124,
       9,   157,    -1,   124,    17,   157,    -1,   124,   157,    -1,
      87,     9,   157,    -1,    87,    17,   157,    -1,    87,   157,
      -1,    79,    17,   157,    -1,    79,   157,    -1,    35,    17,
     157,    -1,    53,     9,   157,    -1,    53,    17,   157,    -1,
      53,   157,    -1,    98,     9,   113,    17,   157,    -1,    98,
       9,   113,   157,    -1,    98,     9,    17,   157,    -1,    98,
       9,   157,    -1,    52,    17,   157,    -1,    52,   157,    -1,
      80,     9,   157,    -1,    18,    17,   157,    -1,    18,     9,
     157,    -1,    18,   157,    -1,    46,    17,   157,    -1,    46,
     157,    -1,   127,    17,   157,    -1,   127,   157,    -1,    33,
      16,   157,    -1,    33,   157,    -1,    71,     9,   157,    -1,
      71,   157,    -1,   115,   151,    -1,   115,    16,   157,    -1,
     115,   159,    69,   157,    -1,    38,    16,   157,    -1,    38,
       9,   157,    -1,    38,   159,    67,    -1,    95,    16,   157,
      -1,    95,     9,   157,    -1,    95,   159,    67,    -1,   140,
       9,   157,    -1,   140,     9,    69,   157,    -1,   140,   159,
      67,    -1,   141,     9,   157,    -1,   143,   157,    -1,   143,
      17,   157,    -1,   143,     9,   157,    -1,   143,     9,     9,
       9,   157,    -1,   122,   157,    -1,    55,   157,    -1,    37,
     157,    -1,    26,   157,    -1,   136,   157,    -1,   106,   157,
      -1,   135,   157,    -1,   128,   157,    -1,    65,   157,    -1,
     138,   157,    -1,    92,   157,    -1,    57,   157,    -1,    42,
     157,    -1,    28,   157,    -1,   134,   157,    -1,    91,   157,
      -1,    77,   157,    -1,    63,   157,    -1,    41,   157,    -1,
      31,   157,    -1,    20,   157,    -1,   125,   157,    -1,   129,
     157,    -1,    51,   157,    -1,    36,   157,    -1,   131,   157,
      -1,   145,   157,    -1,   130,   157,    -1,   121,   157,    -1,
     157,    -1,     9,   157,    -1,   150,    -1,    -1,   158,     9,
      -1,   158,    69,    -1,     9,    -1,   159,     9,    -1,     9,
      -1,   160,     9,    -1,     9,    -1,     9,   126,     9,    -1,
       9,    -1,   162,   161,    -1,   161,    -1
};

/* YYRLINE[YYN] -- source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,    98,    98,    99,   102,   103,   106,   111,   115,   120,
     123,   126,   130,   135,   139,   142,   145,   149,   154,   158,
     162,   167,   171,   174,   178,   182,   186,   191,   196,   201,
     206,   213,   217,   222,   227,   231,   235,   239,   244,   248,
     252,   255,   258,   262,   265,   268,   271,   275,   279,   284,
     287,   291,   295,   299,   303,   308,   312,   317,   321,   327,
     336,   340,   343,   347,   350,   353,   356,   359,   362,   365,
     368,   371,   374,   377,   380,   383,   387,   390,   393,   396,
     399,   402,   405,   408,   411,   414,   417,   420,   424,   429,
     434,   440,   445,   448,   453,   463,   466,   471,   474,   480,
     484,   489,   492,   497,   500,   505,   508,   512,   517,   520,
     525,   528,   534,   538,   543,   546,   554,   559,   567,   572,
     577,   580,   588,   593,   601,   606,   610,   619,   628,   631,
     644,   652,   656,   665,   673,   676,   688,   696,   700,   709,
     717,   720,   732,   740,   744,   753,   761,   764,   776,   784,
     788,   797,   805,   808,   820,   828,   832,   841,   849,   852,
     864,   872,   876,   881,   884,   888,   891,   896,   900,   905,
     908,   913,   916,   926,   931,   934,   938,   943,   946,   951,
     954,   960,   964,   969,   972,   976,   980,   984,   988,   991,
     994,   998,  1003,  1008,  1011,  1016,  1019,  1024,  1028,  1033,
    1036,  1041,  1044,  1048,  1053,  1057,  1061,  1065,  1069,  1073,
    1077,  1081,  1085,  1089,  1092,  1096,  1099,  1105,  1111,  1119,
    1122,  1125,  1128,  1131,  1134,  1137,  1140,  1143,  1146,  1149,
    1152,  1155,  1158,  1161,  1164,  1167,  1170,  1173,  1176,  1179,
    1182,  1185,  1188,  1191,  1194,  1197,  1200,  1203,  1206,  1209,
    1220,  1220,  1222,  1244,  1247,  1252,  1274,  1279,  1305,  1324,
    1328,  1333,  1355
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || YYTOKEN_TABLE
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "APROPOS", "DESCRIBE", "ECHO", "SYSTEM",
  "QUIT", "HFST", "NAMETOKEN", "NAMECHAR", "GLOB", "PROTOTYPE",
  "DEFINE_NAME", "DEFINE_FUNCTION", "RANGE", "REDIRECT_IN", "REDIRECT_OUT",
  "SAVE_PROLOG", "FOR", "REVERSE", "VIEW", "LOADD", "PRINT_LABEL_COUNT",
  "TEST_OVERLAP", "TEST_NONNULL", "CONCATENATE", "LOADS", "INVERT",
  "PRINT_ALIASES", "PRINT_LABELS", "XFST_OPTIONAL",
  "PRINT_SHORTEST_STRING_SIZE", "READ_PROPS", "TEST_FUNCT",
  "PRINT_LABELMAPS", "SUBSTRING", "COMPOSE", "READ_SPACED",
  "TEST_UPPER_UNI", "COLLECT_EPSILON_LOOPS", "ZERO_PLUS", "INSPECT",
  "ROTATE", "PRINT_WORDS", "POP", "SAVE_SPACED", "DEFINE", "SHOW",
  "PRINT_LONGEST_STRING_SIZE", "TEST_EQ", "SORT", "SAVE_DEFINITIONS",
  "SAVE_DOT", "TEST_UPPER_BOUNDED", "COMPLETE", "PRINT_FILE_INFO",
  "INTERSECT", "END_SUB", "TURN", "PRINT_LIST", "SUBSTITUTE_SYMBOL",
  "APPLY_UP", "ONE_PLUS", "UNDEFINE", "EPSILON_REMOVE",
  "PRINT_RANDOM_WORDS", "CTRLD", "EXTRACT_UNAMBIGUOUS", "SEMICOLON",
  "PRINT_LOWER_WORDS", "READ_PROLOG", "CLEAR", "PRINT_SIGMA_COUNT",
  "SUBSTITUTE_NAMED", "PRINT_FLAGS", "SET", "NEGATE", "APPLY_DOWN",
  "PRINT_STACK", "SAVE_STACK", "PUSH", "TEST_LOWER_BOUNDED",
  "PRINT_DEFINED", "APPLY_MED", "SHOW_ALL", "PRINT_ARCCOUNT", "PRINT_SIZE",
  "TEST_NULL", "PRINT_RANDOM_UPPER", "PRINT_LONGEST_STRING", "UPPER_SIDE",
  "XFST_IGNORE", "TEST_UNAMBIGUOUS", "PRINT", "READ_TEXT", "UNLIST",
  "SUBSTITUTE_LABEL", "SAVE_DEFINITION", "ELIMINATE_FLAG", "EDIT_PROPS",
  "PRINT_UPPER_WORDS", "NAME", "EXTRACT_AMBIGUOUS", "DEFINE_ALIAS",
  "PRINT_RANDOM_LOWER", "CROSSPRODUCT", "COMPACT_SIGMA", "SOURCE",
  "AMBIGUOUS", "ELIMINATE_ALL", "PRINT_SIGMA", "PRINT_SHORTEST_STRING",
  "LEFT_PAREN", "PRINT_PROPS", "READ_REGEX", "DEFINE_LIST", "TEST_ID",
  "PRINT_LISTS", "TEST_SUBLANGUAGE", "TEST_LOWER_UNI",
  "COMPILE_REPLACE_UPPER", "CLEANUP", "ADD_PROPS",
  "PRINT_SIGMA_WORD_COUNT", "SHUFFLE", "COLON", "SAVE_TEXT", "DETERMINIZE",
  "SIGMA", "COMPILE_REPLACE_LOWER", "UNION", "PRINT_DIR", "LIST",
  "LOWER_SIDE", "MINIMIZE", "MINUS", "PRINT_NAME", "PRUNE_NET",
  "PUSH_DEFINED", "READ_LEXC", "READ_ATT", "TWOSIDED_FLAGS", "WRITE_ATT",
  "ASSERT", "LABEL_NET", "LOOKUP_OPTIMIZE", "REMOVE_OPTIMIZATION",
  "TEST_INFINITELY_AMBIGUOUS", "XFST_ERROR", "NEWLINE", "REGEX",
  "APPLY_INPUT", "$accept", "XFST_SCRIPT", "COMMAND_LIST", "COMMAND",
  "END_COMMAND", "COMMAND_SEQUENCE", "NAMETOKEN_LIST",
  "QUOTED_NAMETOKEN_LIST", "LABEL", "LABEL_LIST", 0
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[YYLEX-NUM] -- Internal token number corresponding to
   token YYLEX-NUM.  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323,   324,
     325,   326,   327,   328,   329,   330,   331,   332,   333,   334,
     335,   336,   337,   338,   339,   340,   341,   342,   343,   344,
     345,   346,   347,   348,   349,   350,   351,   352,   353,   354,
     355,   356,   357,   358,   359,   360,   361,   362,   363,   364,
     365,   366,   367,   368,   369,   370,   371,   372,   373,   374,
     375,   376,   377,   378,   379,   380,   381,   382,   383,   384,
     385,   386,   387,   388,   389,   390,   391,   392,   393,   394,
     395,   396,   397,   398,   399,   400,   401,   402,   403,   404,
     405,   406,   407
};
# endif

/* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,   153,   154,   154,   155,   155,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     156,   156,   156,   156,   156,   156,   156,   156,   156,   156,
     157,   157,   158,   158,   158,   159,   159,   160,   160,   161,
     161,   162,   162
};

/* YYR2[YYN] -- Number of symbols composing right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     2,     2,     1,     3,     3,     2,     2,
       3,     3,     3,     4,     2,     3,     3,     3,     4,     3,
       3,     4,     2,     2,     2,     2,     2,     4,     5,     5,
       4,     1,     2,     2,     3,     3,     3,     3,     2,     2,
       2,     2,     3,     2,     2,     2,     3,     3,     4,     2,
       2,     3,     2,     1,     1,     1,     3,     1,     2,     4,
       3,     2,     2,     2,     2,     2,     1,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     3,     3,     3,     3,
       3,     3,     3,     3,     3,     3,     3,     3,     5,     5,
       5,     3,     2,     3,     3,     2,     3,     2,     4,     3,
       3,     2,     3,     2,     3,     2,     3,     3,     2,     3,
       2,     4,     3,     3,     2,     3,     2,     3,     2,     3,
       2,     3,     2,     3,     2,     4,     5,     3,     2,     4,
       3,     4,     5,     3,     2,     4,     3,     4,     5,     3,
       2,     4,     3,     4,     5,     3,     2,     4,     3,     4,
       5,     3,     2,     4,     3,     4,     5,     3,     2,     4,
       3,     3,     3,     2,     3,     2,     3,     3,     3,     2,
       3,     2,     3,     3,     2,     3,     3,     2,     3,     2,
       3,     3,     3,     2,     5,     4,     4,     3,     3,     2,
       3,     3,     3,     2,     3,     2,     3,     2,     3,     2,
       3,     2,     2,     3,     4,     3,     3,     3,     3,     3,
       3,     3,     4,     3,     3,     2,     3,     3,     5,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     1,     2,
       1,     0,     2,     2,     1,     2,     1,     2,     1,     3,
       1,     2,     1
};

/* YYDEFACT[STATE-NAME] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE doesn't specify something else to do.  Zero
   means the default is an error.  */
static const yytype_uint16 yydefact[] =
{
     251,   251,   251,    53,    57,    54,    55,   251,    31,     0,
     251,   251,   251,     0,   251,   251,   251,   251,     0,   251,
     251,   251,   251,   251,   251,   251,     0,   251,   251,     0,
     251,   251,   251,   251,   251,   251,   251,   251,     0,   251,
     251,   251,   251,   251,   251,   251,   251,   251,   251,     0,
       0,   251,   251,     0,   251,   251,   251,   251,   251,   251,
     251,     0,   251,     0,   251,   251,   251,     0,   251,   251,
       0,   251,   251,   251,   251,   251,   251,   251,   251,   251,
     251,     0,     0,     0,     0,     0,   251,   251,     0,   251,
       0,   251,   251,   251,     0,   251,   251,   251,   251,   251,
       0,   251,   251,   251,   251,   251,   251,     0,   251,   251,
     251,   251,   251,   251,   251,   251,     0,   251,   251,   251,
     251,   251,   251,     0,     0,   251,   251,     0,   251,   251,
     251,    66,   250,     0,     2,     5,   248,    38,    39,   249,
      32,    33,   251,   251,   193,   239,    58,   251,   251,   110,
      73,    71,   222,   251,   251,   232,   251,    92,   251,   251,
     108,   238,   251,   124,   251,   199,    64,   251,   243,   221,
     251,   251,     0,    70,    49,   237,   231,    45,   251,   251,
     152,    41,   251,   195,   251,   251,   118,    63,   242,   251,
     189,   251,   251,   183,    69,   220,   251,   103,   230,    44,
     251,   258,     0,   251,   251,   251,     9,   236,   256,   251,
     227,   251,   251,   158,    26,   251,   251,   128,   251,   201,
      40,   251,   171,     0,   251,   105,     0,   235,   251,   251,
     251,    14,   251,   179,   251,    67,   251,    97,   251,   251,
       0,    61,   251,   251,    95,   251,   251,   177,    72,   251,
     251,   146,   251,   116,   234,   229,    75,   251,   251,   163,
     251,   251,     0,   251,   260,   262,     0,   251,   251,     8,
     251,   251,   140,   251,    25,     0,   251,   251,   134,   224,
      50,   251,    24,    52,   251,   251,   169,   251,   122,   251,
     251,   165,   251,   202,     0,    65,   251,   114,    74,    68,
     247,   219,   251,     0,   251,   251,   174,   240,   251,   197,
     226,   241,   246,   244,   251,   251,   101,     0,   233,   225,
     223,   251,   120,   228,   251,    43,   251,     0,   251,    62,
     251,   251,   215,   251,   251,   251,   251,   251,   251,   251,
     251,   251,   251,   251,   251,   245,    22,    23,     1,     3,
       4,   192,   191,    37,   109,   251,    47,    46,    91,   106,
     107,   123,   198,   180,   206,   205,   255,   207,   251,   251,
     151,   154,   194,    60,   117,   188,   181,   182,   102,   251,
     112,   257,     0,    11,    12,    10,     0,    34,   251,   251,
     157,   160,   251,   251,   127,   130,   200,   170,     0,   104,
     251,    16,    17,    15,     0,   178,   190,    96,    19,    20,
       0,    94,    93,   175,   176,   251,   251,   145,   148,   115,
     161,   162,   209,   208,   210,    35,     0,     0,   261,   251,
     251,   187,    51,   251,   251,   139,   142,    36,   254,     0,
     251,   251,   251,   133,   136,    56,   167,   168,   121,   164,
     166,   203,   251,   113,     6,     7,   172,   173,   196,   251,
      99,   100,   251,     0,   119,    42,   251,   211,   213,   214,
       0,   217,   216,    85,    83,    77,    82,    76,    81,    79,
      84,    87,    78,    86,    80,    48,   251,   149,   153,   111,
     251,    13,   251,   155,   159,   251,   125,   129,   251,    59,
      18,    21,   251,   143,   147,   259,   251,   186,   251,   185,
     251,   137,   141,     0,   252,   253,    27,   251,   131,   135,
     204,    98,    30,   251,   212,   251,   150,    90,   156,   126,
      88,   144,    89,   184,   138,    28,   132,    29,   218
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,   133,   134,   135,   136,   440,   172,   202,   265,   266
};

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
#define YYPACT_NINF -264
static const yytype_int16 yypact[] =
{
     671,  -143,  -143,  -264,  -264,  -264,  -264,  -143,  -123,  -114,
      -5,  -143,  -143,    40,   -15,  -143,  -143,  -143,   171,  -143,
     -12,   114,  -143,    35,     1,  -143,    -9,  -143,  -143,   203,
    -143,  -143,  -143,  -143,  -143,   131,  -143,   115,    73,   215,
    -143,  -143,   219,   156,  -143,  -143,   226,  -143,  -143,   124,
     135,   121,  -143,   147,  -143,   159,  -143,   162,    39,  -143,
     229,   166,   235,   188,  -143,   127,   251,   197,  -143,   261,
      90,  -143,   165,   196,  -143,   207,   281,  -143,  -143,  -143,
     209,   365,   245,   287,   290,   309,  -143,   230,   363,  -143,
     364,   244,  -143,  -143,   374,  -143,  -143,   246,   293,   273,
      71,  -143,   304,  -143,  -143,  -143,  -143,   366,   276,  -143,
     305,  -143,  -143,  -143,  -143,   181,   375,  -143,  -143,  -143,
     307,  -143,    51,   380,   381,  -143,   285,   798,  -143,  -143,
    -143,  -264,  -264,   393,   523,  -264,  -264,  -264,  -264,  -264,
    -264,  -264,  -143,  -143,  -264,  -264,  -264,  -143,  -143,  -264,
    -264,  -264,  -264,    12,  -143,  -264,  -143,  -264,  -143,  -143,
    -264,  -264,  -143,  -264,  -143,  -264,  -264,  -143,  -264,  -264,
    -143,  -143,    16,  -264,  -264,  -264,  -264,  -264,   288,  -143,
    -264,  -264,  -143,  -264,  -143,  -143,  -264,  -264,  -264,  -143,
    -264,  -143,  -143,  -264,  -264,  -264,  -143,  -264,  -264,  -264,
     327,  -264,   140,  -143,  -143,  -143,   147,  -264,  -264,    75,
    -264,   299,  -143,  -264,  -264,   302,  -143,  -264,  -143,  -264,
    -264,  -143,  -264,   376,  -143,  -264,   388,  -264,  -143,  -143,
    -143,   147,  -143,  -264,  -143,  -264,  -143,  -264,  -143,  -143,
     147,  -264,  -143,  -143,  -264,  -143,  -143,  -264,  -264,   336,
    -143,  -264,  -143,  -264,  -264,  -264,  -264,  -143,  -143,  -264,
    -143,  -143,   191,  -143,   272,  -264,   141,   137,  -143,  -264,
     338,  -143,  -264,  -143,  -264,    80,   343,  -143,  -264,  -264,
    -264,  -143,  -264,  -264,  -143,  -143,  -264,  -143,  -264,  -143,
    -143,  -264,  -143,  -264,    53,  -264,  -143,  -264,  -264,  -264,
    -264,  -264,  -143,   291,  -143,  -143,  -264,  -264,  -143,  -264,
    -264,  -264,  -264,  -264,   331,  -143,  -264,   362,  -264,  -264,
    -264,  -143,  -264,  -264,  -143,  -264,    46,   319,  -143,  -264,
      84,  -143,  -264,  -143,  -143,  -143,  -143,  -143,  -143,  -143,
    -143,  -143,  -143,  -143,  -143,  -264,  -264,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -143,  -264,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,   332,  -143,
    -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -143,
    -264,  -264,   391,  -264,  -264,  -264,   163,  -264,   333,  -143,
    -264,  -264,   334,  -143,  -264,  -264,  -264,  -264,   395,  -264,
    -143,  -264,  -264,  -264,   347,  -264,  -264,  -264,  -264,  -264,
     352,  -264,  -264,  -264,  -264,   345,  -143,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -264,   397,   287,  -264,  -143,
     346,  -264,  -264,   349,  -143,  -264,  -264,  -264,  -264,   147,
      57,   353,  -143,  -264,  -264,  -264,  -264,  -264,  -264,  -264,
    -264,  -264,  -143,  -264,  -264,  -264,  -264,  -264,  -264,  -143,
    -264,  -264,  -143,   125,  -264,  -264,  -143,  -264,  -264,  -264,
     398,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -264,  -143,  -264,  -264,  -264,
    -143,  -264,  -143,  -264,  -264,  -143,  -264,  -264,  -143,  -264,
    -264,  -264,  -143,  -264,  -264,  -264,  -143,  -264,  -143,  -264,
    -143,  -264,  -264,   355,  -264,  -264,  -264,  -143,  -264,  -264,
    -264,  -264,  -264,  -143,  -264,  -143,  -264,  -264,  -264,  -264,
    -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264,  -264
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -264,  -264,  -264,   268,    -1,  -264,    86,  -264,  -263,  -264
};

/* YYTABLE[YYPACT[STATE-NUM]].  What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule which
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
#define YYTABLE_NINF -1
static const yytype_uint16 yytable[] =
{
     137,   138,   148,   428,   142,   156,   139,   132,   167,   144,
     145,   146,   143,   149,   150,   151,   152,   164,   155,   157,
     160,   161,   163,   165,   166,   366,   168,   169,   140,   173,
     174,   175,   176,   177,   180,   181,   183,   141,   186,   187,
     188,   190,   193,   194,   195,   197,   198,   199,   218,   147,
     206,   207,   162,   210,   213,   214,   217,   219,   220,   222,
     324,   225,   366,   227,   231,   233,   514,   235,   237,   240,
     241,   244,   247,   248,   251,   253,   254,   255,   256,   259,
     208,   355,   184,   367,   366,   269,   272,   292,   274,   438,
     278,   279,   280,   470,   282,   283,   286,   288,   291,   238,
     295,   297,   298,   299,   300,   301,   239,   306,   307,   309,
     310,   311,   312,   313,   316,   466,   318,   319,   320,   322,
     323,   325,   452,   158,   329,   332,   515,   345,   346,   347,
     203,   159,   182,   200,   366,   132,   228,   204,   132,   209,
     178,   351,   352,   229,   201,   132,   353,   354,   179,   381,
     264,   132,   356,   357,   429,   358,   208,   359,   360,   382,
     427,   361,   132,   362,   506,   191,   363,   262,   211,   364,
     365,   215,   366,   192,   242,   223,   212,   370,   371,   216,
     153,   372,   243,   373,   374,   132,   294,   154,   375,   132,
     376,   377,   314,   303,   523,   378,   132,   226,   315,   380,
     366,   132,   383,   384,   385,   245,   234,   132,   387,   327,
     390,   391,   170,   246,   394,   395,   249,   396,   257,   171,
     397,   491,   293,   399,   250,   132,   258,   401,   402,   403,
     132,   405,   185,   406,   132,   407,   189,   408,   409,   270,
     132,   411,   412,   196,   413,   414,   221,   271,   417,   418,
     430,   419,   224,   276,   263,   284,   420,   421,   424,   422,
     423,   277,   425,   285,   132,   132,   431,   432,   232,   435,
     436,   132,   437,   205,   439,   443,   444,   132,   236,   230,
     445,   132,   289,   446,   447,   304,   448,   132,   449,   450,
     290,   451,   386,   305,   330,   453,   264,   368,   252,   267,
     366,   454,   331,   456,   457,   369,   132,   458,   388,   132,
     287,   392,   132,   460,   461,   132,   389,   404,   268,   393,
     464,   296,   308,   465,   321,   467,   410,   469,   366,   471,
     472,   132,   473,   474,   475,   476,   477,   478,   479,   480,
     481,   482,   483,   484,   379,   415,   132,   433,   459,   486,
     492,   495,   441,   416,   485,   434,   366,   132,   455,   132,
     442,   366,   502,   508,   366,   132,   510,   487,   488,   132,
     517,   208,   273,   275,   260,   208,   132,   462,   489,   132,
     132,   261,   302,   281,   317,   132,   468,   493,   494,   326,
     328,   496,   497,   348,   132,   398,   132,   400,   426,   499,
     490,   132,   350,   463,   498,   500,   505,   525,     0,     0,
     501,   132,     0,   535,   503,   504,     0,     0,     0,     0,
       0,     0,     0,   132,     0,     0,   132,     0,   507,   509,
       0,   132,   511,   512,     0,   132,     0,     0,   132,   516,
     518,   519,     0,   132,     0,     0,     0,     0,     0,   132,
       0,   520,   132,     0,   132,   132,     0,   132,   521,     0,
       0,   522,     0,     0,     0,   524,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,   132,     0,     0,
       0,   132,   132,   132,   132,   526,   132,     0,   132,   527,
       0,   528,     0,   132,   529,   132,   132,   530,     0,   132,
       0,   531,     0,   132,     0,   532,     0,   533,     0,   534,
       0,     0,     0,     0,     0,     0,   536,     0,     0,     0,
       0,     0,   537,     0,   538,   513,     1,     2,     3,     4,
       5,     6,     7,     0,     0,     0,     8,     9,     0,     0,
       0,    10,     0,    11,    12,    13,    14,    15,    16,    17,
      18,    19,    20,    21,    22,    23,    24,    25,    26,    27,
      28,    29,    30,    31,    32,    33,    34,    35,    36,    37,
       0,    38,    39,    40,    41,    42,    43,    44,    45,    46,
      47,     0,    48,    49,    50,    51,    52,    53,    54,    55,
     349,    56,     0,    57,    58,    59,    60,    61,    62,    63,
      64,    65,    66,    67,     0,    68,    69,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    81,    82,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
      93,    94,    95,    96,    97,    98,     0,    99,   100,     0,
     101,   102,   103,   104,   105,   106,   107,   108,   109,     0,
     110,   111,   112,   113,   114,   115,   116,   117,   118,   119,
     120,   121,   122,   123,   124,   125,   126,   127,   128,   129,
     130,   131,     0,   132,     1,     2,     3,     4,     5,     6,
       7,     0,     0,     0,     8,     9,     0,     0,     0,    10,
       0,    11,    12,    13,    14,    15,    16,    17,    18,    19,
      20,    21,    22,    23,    24,    25,    26,    27,    28,    29,
      30,    31,    32,    33,    34,    35,    36,    37,     0,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    47,     0,
      48,    49,    50,    51,    52,    53,    54,    55,     0,    56,
       0,    57,    58,    59,    60,    61,    62,    63,    64,    65,
      66,    67,     0,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,     0,    99,   100,     0,   101,   102,
     103,   104,   105,   106,   107,   108,   109,     0,   110,   111,
     112,   113,   114,   115,   116,   117,   118,   119,   120,   121,
     122,   123,   124,   125,   126,   127,   128,   129,   130,   131,
       0,   132,   333,   334,     0,     0,     0,     0,     0,     0,
       0,     0,   335,     0,     0,     0,     0,   336,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,   337,     0,
       0,     0,   338,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     339,     0,     0,     0,     0,     0,   340,     0,     0,     0,
       0,   341,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,   342,     0,   343,   344
};

#define yypact_value_is_default(yystate) \
  ((yystate) == (-264))

#define yytable_value_is_error(yytable_value) \
  YYID (0)

static const yytype_int16 yycheck[] =
{
       1,     2,    17,   266,     9,    17,     7,   150,    17,    10,
      11,    12,    17,    14,    15,    16,    17,    16,    19,    20,
      21,    22,    23,    24,    25,     9,    27,    28,   151,    30,
      31,    32,    33,    34,    35,    36,    37,   151,    39,    40,
      41,    42,    43,    44,    45,    46,    47,    48,     9,     9,
      51,    52,    17,    54,    55,    56,    57,    58,    59,    60,
       9,    62,     9,    64,    65,    66,     9,    68,    69,    70,
      71,    72,    73,    74,    75,    76,    77,    78,    79,    80,
       9,    69,     9,    67,     9,    86,    87,    16,    89,     9,
      91,    92,    93,     9,    95,    96,    97,    98,    99,     9,
     101,   102,   103,   104,   105,   106,    16,   108,   109,   110,
     111,   112,   113,   114,   115,    69,   117,   118,   119,   120,
     121,   122,    69,     9,   125,   126,    69,   128,   129,   130,
       9,    17,    17,     9,     9,   150,     9,    16,   150,    53,
       9,   142,   143,    16,     9,   150,   147,   148,    17,     9,
       9,   150,   153,   154,    17,   156,     9,   158,   159,    19,
      19,   162,   150,   164,   427,     9,   167,    81,     9,   170,
     171,     9,     9,    17,     9,     9,    17,   178,   179,    17,
       9,   182,    17,   184,   185,   150,   100,    16,   189,   150,
     191,   192,    11,   107,    69,   196,   150,     9,    17,   200,
       9,   150,   203,   204,   205,     9,     9,   150,   209,   123,
     211,   212,     9,    17,   215,   216,     9,   218,     9,    16,
     221,    58,   151,   224,    17,   150,    17,   228,   229,   230,
     150,   232,    17,   234,   150,   236,    17,   238,   239,     9,
     150,   242,   243,    17,   245,   246,    17,    17,   249,   250,
     113,   252,    17,     9,     9,     9,   257,   258,    67,   260,
     261,    17,   263,    17,   150,   150,   267,   268,    17,   270,
     271,   150,   273,   152,   275,   276,   277,   150,    17,   152,
     281,   150,     9,   284,   285,     9,   287,   150,   289,   290,
      17,   292,   206,    17,     9,   296,     9,     9,    17,     9,
       9,   302,    17,   304,   305,    17,   150,   308,     9,   150,
      17,     9,   150,   314,   315,   150,    17,   231,     9,    17,
     321,    17,    17,   324,    17,   326,   240,   328,     9,   330,
     331,   150,   333,   334,   335,   336,   337,   338,   339,   340,
     341,   342,   343,   344,    17,     9,   150,     9,    17,    17,
      17,    17,     9,    17,   355,    17,     9,   150,    67,   150,
      17,     9,    17,    17,     9,   150,    17,   368,   369,   150,
      17,     9,     9,     9,     9,     9,   150,    15,   379,   150,
     150,    16,    16,     9,     9,   150,    67,   388,   389,     9,
       9,   392,   393,     0,   150,    19,   150,     9,   126,   400,
       9,   150,   134,   317,     9,    58,     9,     9,    -1,    -1,
      58,   150,    -1,    58,   415,   416,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,   150,    -1,    -1,   150,    -1,   429,   430,
      -1,   150,   433,   434,    -1,   150,    -1,    -1,   150,   440,
     441,   442,    -1,   150,    -1,    -1,    -1,    -1,    -1,   150,
      -1,   452,   150,    -1,   150,   150,    -1,   150,   459,    -1,
      -1,   462,    -1,    -1,    -1,   466,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,   150,    -1,    -1,
      -1,   150,   150,   150,   150,   486,   150,    -1,   150,   490,
      -1,   492,    -1,   150,   495,   150,   150,   498,    -1,   150,
      -1,   502,    -1,   150,    -1,   506,    -1,   508,    -1,   510,
      -1,    -1,    -1,    -1,    -1,    -1,   517,    -1,    -1,    -1,
      -1,    -1,   523,    -1,   525,   439,     3,     4,     5,     6,
       7,     8,     9,    -1,    -1,    -1,    13,    14,    -1,    -1,
      -1,    18,    -1,    20,    21,    22,    23,    24,    25,    26,
      27,    28,    29,    30,    31,    32,    33,    34,    35,    36,
      37,    38,    39,    40,    41,    42,    43,    44,    45,    46,
      -1,    48,    49,    50,    51,    52,    53,    54,    55,    56,
      57,    -1,    59,    60,    61,    62,    63,    64,    65,    66,
      67,    68,    -1,    70,    71,    72,    73,    74,    75,    76,
      77,    78,    79,    80,    -1,    82,    83,    84,    85,    86,
      87,    88,    89,    90,    91,    92,    93,    94,    95,    96,
      97,    98,    99,   100,   101,   102,   103,   104,   105,   106,
     107,   108,   109,   110,   111,   112,    -1,   114,   115,    -1,
     117,   118,   119,   120,   121,   122,   123,   124,   125,    -1,
     127,   128,   129,   130,   131,   132,   133,   134,   135,   136,
     137,   138,   139,   140,   141,   142,   143,   144,   145,   146,
     147,   148,    -1,   150,     3,     4,     5,     6,     7,     8,
       9,    -1,    -1,    -1,    13,    14,    -1,    -1,    -1,    18,
      -1,    20,    21,    22,    23,    24,    25,    26,    27,    28,
      29,    30,    31,    32,    33,    34,    35,    36,    37,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    -1,    48,
      49,    50,    51,    52,    53,    54,    55,    56,    57,    -1,
      59,    60,    61,    62,    63,    64,    65,    66,    -1,    68,
      -1,    70,    71,    72,    73,    74,    75,    76,    77,    78,
      79,    80,    -1,    82,    83,    84,    85,    86,    87,    88,
      89,    90,    91,    92,    93,    94,    95,    96,    97,    98,
      99,   100,   101,   102,   103,   104,   105,   106,   107,   108,
     109,   110,   111,   112,    -1,   114,   115,    -1,   117,   118,
     119,   120,   121,   122,   123,   124,   125,    -1,   127,   128,
     129,   130,   131,   132,   133,   134,   135,   136,   137,   138,
     139,   140,   141,   142,   143,   144,   145,   146,   147,   148,
      -1,   150,    24,    25,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    34,    -1,    -1,    -1,    -1,    39,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    50,    -1,
      -1,    -1,    54,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      82,    -1,    -1,    -1,    -1,    -1,    88,    -1,    -1,    -1,
      -1,    93,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,   117,    -1,   119,   120
};

/* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
   symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     3,     4,     5,     6,     7,     8,     9,    13,    14,
      18,    20,    21,    22,    23,    24,    25,    26,    27,    28,
      29,    30,    31,    32,    33,    34,    35,    36,    37,    38,
      39,    40,    41,    42,    43,    44,    45,    46,    48,    49,
      50,    51,    52,    53,    54,    55,    56,    57,    59,    60,
      61,    62,    63,    64,    65,    66,    68,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    79,    80,    82,    83,
      84,    85,    86,    87,    88,    89,    90,    91,    92,    93,
      94,    95,    96,    97,    98,    99,   100,   101,   102,   103,
     104,   105,   106,   107,   108,   109,   110,   111,   112,   114,
     115,   117,   118,   119,   120,   121,   122,   123,   124,   125,
     127,   128,   129,   130,   131,   132,   133,   134,   135,   136,
     137,   138,   139,   140,   141,   142,   143,   144,   145,   146,
     147,   148,   150,   154,   155,   156,   157,   157,   157,   157,
     151,   151,     9,    17,   157,   157,   157,     9,    17,   157,
     157,   157,   157,     9,    16,   157,    17,   157,     9,    17,
     157,   157,    17,   157,    16,   157,   157,    17,   157,   157,
       9,    16,   159,   157,   157,   157,   157,   157,     9,    17,
     157,   157,    17,   157,     9,    17,   157,   157,   157,    17,
     157,     9,    17,   157,   157,   157,    17,   157,   157,   157,
       9,     9,   160,     9,    16,   152,   157,   157,     9,   159,
     157,     9,    17,   157,   157,     9,    17,   157,     9,   157,
     157,    17,   157,     9,    17,   157,     9,   157,     9,    16,
     152,   157,    17,   157,     9,   157,    17,   157,     9,    16,
     157,   157,     9,    17,   157,     9,    17,   157,   157,     9,
      17,   157,    17,   157,   157,   157,   157,     9,    17,   157,
       9,    16,   159,     9,     9,   161,   162,     9,     9,   157,
       9,    17,   157,     9,   157,     9,     9,    17,   157,   157,
     157,     9,   157,   157,     9,    17,   157,    17,   157,     9,
      17,   157,    16,   151,   159,   157,    17,   157,   157,   157,
     157,   157,    16,   159,     9,    17,   157,   157,    17,   157,
     157,   157,   157,   157,    11,    17,   157,     9,   157,   157,
     157,    17,   157,   157,     9,   157,     9,   159,     9,   157,
       9,    17,   157,    24,    25,    34,    39,    50,    54,    82,
      88,    93,   117,   119,   120,   157,   157,   157,     0,    67,
     156,   157,   157,   157,   157,    69,   157,   157,   157,   157,
     157,   157,   157,   157,   157,   157,     9,    67,     9,    17,
     157,   157,   157,   157,   157,   157,   157,   157,   157,    17,
     157,     9,    19,   157,   157,   157,   159,   157,     9,    17,
     157,   157,     9,    17,   157,   157,   157,   157,    19,   157,
       9,   157,   157,   157,   159,   157,   157,   157,   157,   157,
     159,   157,   157,   157,   157,     9,    17,   157,   157,   157,
     157,   157,   157,   157,    67,   157,   126,    19,   161,    17,
     113,   157,   157,     9,    17,   157,   157,   157,     9,   157,
     158,     9,    17,   157,   157,   157,   157,   157,   157,   157,
     157,   157,    69,   157,   157,    67,   157,   157,   157,    17,
     157,   157,    15,   159,   157,   157,    69,   157,    67,   157,
       9,   157,   157,   157,   157,   157,   157,   157,   157,   157,
     157,   157,   157,   157,   157,   157,    17,   157,   157,   157,
       9,    58,    17,   157,   157,    17,   157,   157,     9,   157,
      58,    58,    17,   157,   157,     9,   161,   157,    17,   157,
      17,   157,   157,   159,     9,    69,   157,    17,   157,   157,
     157,   157,   157,    69,   157,     9,   157,   157,   157,   157,
     157,   157,   157,   157,   157,    58,   157,   157,   157
};

#define yyerrok		(yyerrstatus = 0)
#define yyclearin	(yychar = YYEMPTY)
#define YYEMPTY		(-2)
#define YYEOF		0

#define YYACCEPT	goto yyacceptlab
#define YYABORT		goto yyabortlab
#define YYERROR		goto yyerrorlab


/* Like YYERROR except do call yyerror.  This remains here temporarily
   to ease the transition to the new meaning of YYERROR, for GCC.
   Once GCC version 2 has supplanted version 1, this can go.  However,
   YYFAIL appears to be in use.  Nevertheless, it is formally deprecated
   in Bison 2.4.2's NEWS entry, where a plan to phase it out is
   discussed.  */

#define YYFAIL		goto yyerrlab
#if defined YYFAIL
  /* This is here to suppress warnings from the GCC cpp's
     -Wunused-macros.  Normally we don't worry about that warning, but
     some users do, and we want to make it easy for users to remove
     YYFAIL uses, which will produce warnings from Bison 2.5.  */
#endif

#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)					\
do								\
  if (yychar == YYEMPTY && yylen == 1)				\
    {								\
      yychar = (Token);						\
      yylval = (Value);						\
      YYPOPSTACK (1);						\
      goto yybackup;						\
    }								\
  else								\
    {								\
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;							\
    }								\
while (YYID (0))


#define YYTERROR	1
#define YYERRCODE	256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#define YYRHSLOC(Rhs, K) ((Rhs)[K])
#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)				\
    do									\
      if (YYID (N))                                                    \
	{								\
	  (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;	\
	  (Current).first_column = YYRHSLOC (Rhs, 1).first_column;	\
	  (Current).last_line    = YYRHSLOC (Rhs, N).last_line;		\
	  (Current).last_column  = YYRHSLOC (Rhs, N).last_column;	\
	}								\
      else								\
	{								\
	  (Current).first_line   = (Current).last_line   =		\
	    YYRHSLOC (Rhs, 0).last_line;				\
	  (Current).first_column = (Current).last_column =		\
	    YYRHSLOC (Rhs, 0).last_column;				\
	}								\
    while (YYID (0))
#endif


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
#  define YY_LOCATION_PRINT(File, Loc)			\
     fprintf (File, "%d.%d-%d.%d",			\
	      (Loc).first_line, (Loc).first_column,	\
	      (Loc).last_line,  (Loc).last_column)
# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


/* YYLEX -- calling `yylex' with the right arguments.  */

#ifdef YYLEX_PARAM
# define YYLEX yylex (YYLEX_PARAM)
#else
# define YYLEX yylex ()
#endif

/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)			\
do {						\
  if (yydebug)					\
    YYFPRINTF Args;				\
} while (YYID (0))

# define YY_SYMBOL_PRINT(Title, Type, Value, Location)			  \
do {									  \
  if (yydebug)								  \
    {									  \
      YYFPRINTF (stderr, "%s ", Title);					  \
      yy_symbol_print (stderr,						  \
		  Type, Value, Location); \
      YYFPRINTF (stderr, "\n");						  \
    }									  \
} while (YYID (0))


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp)
#else
static void
yy_symbol_value_print (yyoutput, yytype, yyvaluep, yylocationp)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
    YYLTYPE const * const yylocationp;
#endif
{
  if (!yyvaluep)
    return;
  YYUSE (yylocationp);
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# else
  YYUSE (yyoutput);
# endif
  switch (yytype)
    {
      default:
	break;
    }
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp)
#else
static void
yy_symbol_print (yyoutput, yytype, yyvaluep, yylocationp)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
    YYLTYPE const * const yylocationp;
#endif
{
  if (yytype < YYNTOKENS)
    YYFPRINTF (yyoutput, "token %s (", yytname[yytype]);
  else
    YYFPRINTF (yyoutput, "nterm %s (", yytname[yytype]);

  YY_LOCATION_PRINT (yyoutput, *yylocationp);
  YYFPRINTF (yyoutput, ": ");
  yy_symbol_value_print (yyoutput, yytype, yyvaluep, yylocationp);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
#else
static void
yy_stack_print (yybottom, yytop)
    yytype_int16 *yybottom;
    yytype_int16 *yytop;
#endif
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)				\
do {								\
  if (yydebug)							\
    yy_stack_print ((Bottom), (Top));				\
} while (YYID (0))


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_reduce_print (YYSTYPE *yyvsp, YYLTYPE *yylsp, int yyrule)
#else
static void
yy_reduce_print (yyvsp, yylsp, yyrule)
    YYSTYPE *yyvsp;
    YYLTYPE *yylsp;
    int yyrule;
#endif
{
  int yynrhs = yyr2[yyrule];
  int yyi;
  unsigned long int yylno = yyrline[yyrule];
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
	     yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr, yyrhs[yyprhs[yyrule] + yyi],
		       &(yyvsp[(yyi + 1) - (yynrhs)])
		       , &(yylsp[(yyi + 1) - (yynrhs)])		       );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)		\
do {					\
  if (yydebug)				\
    yy_reduce_print (yyvsp, yylsp, Rule); \
} while (YYID (0))

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef	YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static YYSIZE_T
yystrlen (const char *yystr)
#else
static YYSIZE_T
yystrlen (yystr)
    const char *yystr;
#endif
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static char *
yystpcpy (char *yydest, const char *yysrc)
#else
static char *
yystpcpy (yydest, yysrc)
    char *yydest;
    const char *yysrc;
#endif
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
	switch (*++yyp)
	  {
	  case '\'':
	  case ',':
	    goto do_not_strip_quotes;

	  case '\\':
	    if (*++yyp != '\\')
	      goto do_not_strip_quotes;
	    /* Fall through.  */
	  default:
	    if (yyres)
	      yyres[yyn] = *yyp;
	    yyn++;
	    break;

	  case '"':
	    if (yyres)
	      yyres[yyn] = '\0';
	    return yyn;
	  }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYSIZE_T *yymsg_alloc, char **yymsg,
                yytype_int16 *yyssp, int yytoken)
{
  YYSIZE_T yysize0 = yytnamerr (0, yytname[yytoken]);
  YYSIZE_T yysize = yysize0;
  YYSIZE_T yysize1;
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = 0;
  /* Arguments of yyformat. */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Number of reported tokens (one for the "unexpected", one per
     "expected"). */
  int yycount = 0;

  /* There are many possibilities here to consider:
     - Assume YYFAIL is not used.  It's too flawed to consider.  See
       <http://lists.gnu.org/archive/html/bison-patches/2009-12/msg00024.html>
       for details.  YYERROR is fine as it does not invoke this
       function.
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[*yyssp];
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                yysize1 = yysize + yytnamerr (0, yytname[yyx]);
                if (! (yysize <= yysize1
                       && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
                  return 2;
                yysize = yysize1;
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  yysize1 = yysize + yystrlen (yyformat);
  if (! (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
    return 2;
  yysize = yysize1;

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          yyp++;
          yyformat++;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep, YYLTYPE *yylocationp)
#else
static void
yydestruct (yymsg, yytype, yyvaluep, yylocationp)
    const char *yymsg;
    int yytype;
    YYSTYPE *yyvaluep;
    YYLTYPE *yylocationp;
#endif
{
  YYUSE (yyvaluep);
  YYUSE (yylocationp);

  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  switch (yytype)
    {

      default:
	break;
    }
}


/* Prevent warnings from -Wmissing-prototypes.  */
#ifdef YYPARSE_PARAM
#if defined __STDC__ || defined __cplusplus
int yyparse (void *YYPARSE_PARAM);
#else
int yyparse ();
#endif
#else /* ! YYPARSE_PARAM */
#if defined __STDC__ || defined __cplusplus
int yyparse (void);
#else
int yyparse ();
#endif
#endif /* ! YYPARSE_PARAM */


/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;

/* Location data for the lookahead symbol.  */
YYLTYPE yylloc;

/* Number of syntax errors so far.  */
int yynerrs;


/*----------.
| yyparse.  |
`----------*/

#ifdef YYPARSE_PARAM
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void *YYPARSE_PARAM)
#else
int
yyparse (YYPARSE_PARAM)
    void *YYPARSE_PARAM;
#endif
#else /* ! YYPARSE_PARAM */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void)
#else
int
yyparse ()

#endif
#endif
{
    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       `yyss': related to states.
       `yyvs': related to semantic values.
       `yyls': related to locations.

       Refer to the stacks thru separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    /* The location stack.  */
    YYLTYPE yylsa[YYINITDEPTH];
    YYLTYPE *yyls;
    YYLTYPE *yylsp;

    /* The locations where the error started and ended.  */
    YYLTYPE yyerror_range[3];

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;
  YYLTYPE yyloc;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N), yylsp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yytoken = 0;
  yyss = yyssa;
  yyvs = yyvsa;
  yyls = yylsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */

  /* Initialize stack pointers.
     Waste one element of value and location stack
     so that they stay on the same level as the state stack.
     The wasted elements are never initialized.  */
  yyssp = yyss;
  yyvsp = yyvs;
  yylsp = yyls;

#if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
  /* Initialize the default location before parsing starts.  */
  yylloc.first_line   = yylloc.last_line   = 1;
  yylloc.first_column = yylloc.last_column = 1;
#endif

  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
	/* Give user a chance to reallocate the stack.  Use copies of
	   these so that the &'s don't force the real ones into
	   memory.  */
	YYSTYPE *yyvs1 = yyvs;
	yytype_int16 *yyss1 = yyss;
	YYLTYPE *yyls1 = yyls;

	/* Each stack pointer address is followed by the size of the
	   data in use in that stack, in bytes.  This used to be a
	   conditional around just the two extra args, but that might
	   be undefined if yyoverflow is a macro.  */
	yyoverflow (YY_("memory exhausted"),
		    &yyss1, yysize * sizeof (*yyssp),
		    &yyvs1, yysize * sizeof (*yyvsp),
		    &yyls1, yysize * sizeof (*yylsp),
		    &yystacksize);

	yyls = yyls1;
	yyss = yyss1;
	yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
	goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
	yystacksize = YYMAXDEPTH;

      {
	yytype_int16 *yyss1 = yyss;
	union yyalloc *yyptr =
	  (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
	if (! yyptr)
	  goto yyexhaustedlab;
	YYSTACK_RELOCATE (yyss_alloc, yyss);
	YYSTACK_RELOCATE (yyvs_alloc, yyvs);
	YYSTACK_RELOCATE (yyls_alloc, yyls);
#  undef YYSTACK_RELOCATE
	if (yyss1 != yyssa)
	  YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;
      yylsp = yyls + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
		  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
	YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = YYLEX;
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  *++yyvsp = yylval;
  *++yylsp = yylloc;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     `$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];

  /* Default location.  */
  YYLLOC_DEFAULT (yyloc, (yylsp - yylen), yylen);
  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 6:

/* Line 1806 of yacc.c  */
#line 106 "xfst-parser.yy"
    {
            FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[(2) - (3)].file), "r"); CHECK;
            hfst::xfst::xfst_->add_props(f);
            hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 7:

/* Line 1806 of yacc.c  */
#line 111 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->add_props((yyvsp[(2) - (3)].text));
            free((yyvsp[(2) - (3)].text)); CHECK;
       }
    break;

  case 8:

/* Line 1806 of yacc.c  */
#line 115 "xfst-parser.yy"
    {
            hxfsterror("NETWORK PROPERTY EDITOR unimplemented\n");
            return EXIT_FAILURE;
       }
    break;

  case 9:

/* Line 1806 of yacc.c  */
#line 120 "xfst-parser.yy"
    {
       	    hfst::xfst::xfst_->apply_up(stdin); CHECK;
       }
    break;

  case 10:

/* Line 1806 of yacc.c  */
#line 123 "xfst-parser.yy"
    {
       	    hfst::xfst::xfst_->apply_up((yyvsp[(2) - (3)].text)); CHECK; free((yyvsp[(2) - (3)].text));
       }
    break;

  case 11:

/* Line 1806 of yacc.c  */
#line 126 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->apply_up((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 12:

/* Line 1806 of yacc.c  */
#line 130 "xfst-parser.yy"
    {
            FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[(2) - (3)].file), "r"); CHECK;
            hfst::xfst::xfst_->apply_up(f);
            hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 13:

/* Line 1806 of yacc.c  */
#line 135 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->apply_up((yyvsp[(3) - (4)].text));
            free((yyvsp[(3) - (4)].text)); CHECK;
       }
    break;

  case 14:

/* Line 1806 of yacc.c  */
#line 139 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->apply_down(stdin); CHECK;
       }
    break;

  case 15:

/* Line 1806 of yacc.c  */
#line 142 "xfst-parser.yy"
    {
       	    hfst::xfst::xfst_->apply_down((yyvsp[(2) - (3)].text)); CHECK; free((yyvsp[(2) - (3)].text));
       }
    break;

  case 16:

/* Line 1806 of yacc.c  */
#line 145 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->apply_down((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 17:

/* Line 1806 of yacc.c  */
#line 149 "xfst-parser.yy"
    {
            FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[(2) - (3)].file), "r"); CHECK;
            hfst::xfst::xfst_->apply_down(f);
            hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 18:

/* Line 1806 of yacc.c  */
#line 154 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->apply_down((yyvsp[(3) - (4)].text));
            free((yyvsp[(3) - (4)].text)); CHECK;
       }
    break;

  case 19:

/* Line 1806 of yacc.c  */
#line 158 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->apply_med((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 20:

/* Line 1806 of yacc.c  */
#line 162 "xfst-parser.yy"
    {
            FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[(2) - (3)].file), "r"); CHECK;
            hfst::xfst::xfst_->apply_med(f);
            hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 21:

/* Line 1806 of yacc.c  */
#line 167 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->apply_med((yyvsp[(3) - (4)].text));
            free((yyvsp[(3) - (4)].text)); CHECK;
       }
    break;

  case 22:

/* Line 1806 of yacc.c  */
#line 171 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->lookup_optimize(); CHECK;
       }
    break;

  case 23:

/* Line 1806 of yacc.c  */
#line 174 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->remove_optimization(); CHECK;
       }
    break;

  case 24:

/* Line 1806 of yacc.c  */
#line 178 "xfst-parser.yy"
    {
            hxfsterror("unimplemetend ambiguous\n");
            return EXIT_FAILURE;
       }
    break;

  case 25:

/* Line 1806 of yacc.c  */
#line 182 "xfst-parser.yy"
    {
            hxfsterror("unimplemetend ambiguous\n");
            return EXIT_FAILURE;
       }
    break;

  case 26:

/* Line 1806 of yacc.c  */
#line 186 "xfst-parser.yy"
    {
            hxfsterror("unimplemetend ambiguous\n");
            return EXIT_FAILURE;
       }
    break;

  case 27:

/* Line 1806 of yacc.c  */
#line 191 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->define_alias((yyvsp[(2) - (4)].name), (yyvsp[(3) - (4)].text));
            free((yyvsp[(2) - (4)].name));
            free((yyvsp[(3) - (4)].text)); CHECK;
       }
    break;

  case 28:

/* Line 1806 of yacc.c  */
#line 196 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->define_alias((yyvsp[(2) - (5)].name), (yyvsp[(4) - (5)].text));
            free((yyvsp[(2) - (5)].name));
            free((yyvsp[(4) - (5)].text)); CHECK;
       }
    break;

  case 29:

/* Line 1806 of yacc.c  */
#line 201 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->define_list((yyvsp[(2) - (5)].name), (yyvsp[(3) - (5)].text));
            free((yyvsp[(2) - (5)].name));
            free((yyvsp[(3) - (5)].text)); CHECK;
       }
    break;

  case 30:

/* Line 1806 of yacc.c  */
#line 206 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->define_list((yyvsp[(2) - (4)].name), (yyvsp[(3) - (4)].list)[0], (yyvsp[(3) - (4)].list)[1]);
            free((yyvsp[(2) - (4)].name));
            free((yyvsp[(3) - (4)].list)[0]);
            free((yyvsp[(3) - (4)].list)[1]);
            free((yyvsp[(3) - (4)].list)); CHECK;
       }
    break;

  case 31:

/* Line 1806 of yacc.c  */
#line 213 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->define((yyvsp[(1) - (1)].name));
            free((yyvsp[(1) - (1)].name)); CHECK;
       }
    break;

  case 32:

/* Line 1806 of yacc.c  */
#line 217 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->define((yyvsp[(1) - (2)].name), (yyvsp[(2) - (2)].text));
            free((yyvsp[(1) - (2)].name));
            free((yyvsp[(2) - (2)].text)); CHECK;
       }
    break;

  case 33:

/* Line 1806 of yacc.c  */
#line 222 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->define_function((yyvsp[(1) - (2)].name), (yyvsp[(2) - (2)].text));
            free((yyvsp[(1) - (2)].name));
            free((yyvsp[(2) - (2)].text)); CHECK;
       }
    break;

  case 34:

/* Line 1806 of yacc.c  */
#line 227 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->undefine((yyvsp[(2) - (3)].text));
            free((yyvsp[(2) - (3)].text)); CHECK;
       }
    break;

  case 35:

/* Line 1806 of yacc.c  */
#line 231 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->unlist((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 36:

/* Line 1806 of yacc.c  */
#line 235 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->name_net((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 37:

/* Line 1806 of yacc.c  */
#line 239 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->load_definitions((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 38:

/* Line 1806 of yacc.c  */
#line 244 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->apropos((yyvsp[(1) - (2)].text));
            free((yyvsp[(1) - (2)].text)); CHECK;
       }
    break;

  case 39:

/* Line 1806 of yacc.c  */
#line 248 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->describe((yyvsp[(1) - (2)].text)); CHECK;
       }
    break;

  case 40:

/* Line 1806 of yacc.c  */
#line 252 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->clear(); CHECK;
       }
    break;

  case 41:

/* Line 1806 of yacc.c  */
#line 255 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->pop(); CHECK;
       }
    break;

  case 42:

/* Line 1806 of yacc.c  */
#line 258 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->push((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 43:

/* Line 1806 of yacc.c  */
#line 262 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->push(); CHECK;
       }
    break;

  case 44:

/* Line 1806 of yacc.c  */
#line 265 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->turn(); CHECK;
       }
    break;

  case 45:

/* Line 1806 of yacc.c  */
#line 268 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->rotate(); CHECK;
       }
    break;

  case 46:

/* Line 1806 of yacc.c  */
#line 271 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->load_stack((yyvsp[(2) - (3)].file));
            free((yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 47:

/* Line 1806 of yacc.c  */
#line 275 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->load_stack((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 48:

/* Line 1806 of yacc.c  */
#line 279 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->load_stack((yyvsp[(2) - (4)].name));
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 49:

/* Line 1806 of yacc.c  */
#line 284 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->collect_epsilon_loops(); CHECK;
       }
    break;

  case 50:

/* Line 1806 of yacc.c  */
#line 287 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->compact_sigma(); CHECK;
       }
    break;

  case 51:

/* Line 1806 of yacc.c  */
#line 291 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->eliminate_flag((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 52:

/* Line 1806 of yacc.c  */
#line 295 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->eliminate_flags(); CHECK;
       }
    break;

  case 53:

/* Line 1806 of yacc.c  */
#line 299 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->echo((yyvsp[(1) - (1)].text));
            free((yyvsp[(1) - (1)].text)); CHECK;
       }
    break;

  case 54:

/* Line 1806 of yacc.c  */
#line 303 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->quit((yyvsp[(1) - (1)].text));
            free((yyvsp[(1) - (1)].text));
            return EXIT_SUCCESS;
       }
    break;

  case 55:

/* Line 1806 of yacc.c  */
#line 308 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->hfst((yyvsp[(1) - (1)].text));
            free((yyvsp[(1) - (1)].text)); CHECK;
       }
    break;

  case 56:

/* Line 1806 of yacc.c  */
#line 312 "xfst-parser.yy"
    {
            hxfsterror("source not implemented yywrap\n");
            free((yyvsp[(2) - (3)].name));
            return EXIT_FAILURE;
       }
    break;

  case 57:

/* Line 1806 of yacc.c  */
#line 317 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->system((yyvsp[(1) - (1)].text));
            free((yyvsp[(1) - (1)].text)); CHECK;
       }
    break;

  case 58:

/* Line 1806 of yacc.c  */
#line 321 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->view_net(); CHECK;
            //hxfsterror("view not implemented\n");
            //return EXIT_FAILURE;
       }
    break;

  case 59:

/* Line 1806 of yacc.c  */
#line 327 "xfst-parser.yy"
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[(3) - (4)].name));
            if (i != -1)
              hfst::xfst::xfst_->set((yyvsp[(2) - (4)].name), i);
            else
              hfst::xfst::xfst_->set((yyvsp[(2) - (4)].name), (yyvsp[(3) - (4)].name));
            free((yyvsp[(2) - (4)].name));
            free((yyvsp[(3) - (4)].name)); CHECK;
       }
    break;

  case 60:

/* Line 1806 of yacc.c  */
#line 336 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->show((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 61:

/* Line 1806 of yacc.c  */
#line 340 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->show(); CHECK;
       }
    break;

  case 62:

/* Line 1806 of yacc.c  */
#line 343 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->twosided_flags(); CHECK;
       }
    break;

  case 63:

/* Line 1806 of yacc.c  */
#line 347 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_eq(); CHECK;
       }
    break;

  case 64:

/* Line 1806 of yacc.c  */
#line 350 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_funct(); CHECK;
       }
    break;

  case 65:

/* Line 1806 of yacc.c  */
#line 353 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_id(); CHECK;
       }
    break;

  case 66:

/* Line 1806 of yacc.c  */
#line 356 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_infinitely_ambiguous(); CHECK;
       }
    break;

  case 67:

/* Line 1806 of yacc.c  */
#line 359 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_lower_bounded(); CHECK;
       }
    break;

  case 68:

/* Line 1806 of yacc.c  */
#line 362 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_lower_uni(); CHECK;
       }
    break;

  case 69:

/* Line 1806 of yacc.c  */
#line 365 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_upper_bounded(); CHECK;
       }
    break;

  case 70:

/* Line 1806 of yacc.c  */
#line 368 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_upper_uni(); CHECK;
       }
    break;

  case 71:

/* Line 1806 of yacc.c  */
#line 371 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_nonnull(); CHECK;
       }
    break;

  case 72:

/* Line 1806 of yacc.c  */
#line 374 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_null(); CHECK;
       }
    break;

  case 73:

/* Line 1806 of yacc.c  */
#line 377 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_overlap(); CHECK;
       }
    break;

  case 74:

/* Line 1806 of yacc.c  */
#line 380 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_sublanguage(); CHECK;
       }
    break;

  case 75:

/* Line 1806 of yacc.c  */
#line 383 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_unambiguous(); CHECK;
       }
    break;

  case 76:

/* Line 1806 of yacc.c  */
#line 387 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_eq(true); CHECK;
       }
    break;

  case 77:

/* Line 1806 of yacc.c  */
#line 390 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_funct(true); CHECK;
       }
    break;

  case 78:

/* Line 1806 of yacc.c  */
#line 393 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_id(true); CHECK;
       }
    break;

  case 79:

/* Line 1806 of yacc.c  */
#line 396 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_lower_bounded(true); CHECK;
       }
    break;

  case 80:

/* Line 1806 of yacc.c  */
#line 399 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_lower_uni(true); CHECK;
       }
    break;

  case 81:

/* Line 1806 of yacc.c  */
#line 402 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_upper_bounded(true); CHECK;
       }
    break;

  case 82:

/* Line 1806 of yacc.c  */
#line 405 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_upper_uni(true); CHECK;
       }
    break;

  case 83:

/* Line 1806 of yacc.c  */
#line 408 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_nonnull(true); CHECK;
       }
    break;

  case 84:

/* Line 1806 of yacc.c  */
#line 411 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_null(true); CHECK;
       }
    break;

  case 85:

/* Line 1806 of yacc.c  */
#line 414 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_overlap(true); CHECK;
       }
    break;

  case 86:

/* Line 1806 of yacc.c  */
#line 417 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_sublanguage(true); CHECK;
       }
    break;

  case 87:

/* Line 1806 of yacc.c  */
#line 420 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->test_unambiguous(true); CHECK;
       }
    break;

  case 88:

/* Line 1806 of yacc.c  */
#line 424 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->substitute_named((yyvsp[(2) - (5)].name), (yyvsp[(4) - (5)].name)); // TODO!
            free((yyvsp[(2) - (5)].name));
            free((yyvsp[(4) - (5)].name)); CHECK;
       }
    break;

  case 89:

/* Line 1806 of yacc.c  */
#line 429 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->substitute_label((yyvsp[(2) - (5)].text), (yyvsp[(4) - (5)].text));
            free((yyvsp[(2) - (5)].text));
            free((yyvsp[(4) - (5)].text)); CHECK;
       }
    break;

  case 90:

/* Line 1806 of yacc.c  */
#line 434 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->substitute_symbol((yyvsp[(2) - (5)].text), (yyvsp[(4) - (5)].name));
            free((yyvsp[(2) - (5)].text));
            free((yyvsp[(4) - (5)].name)); CHECK;
       }
    break;

  case 91:

/* Line 1806 of yacc.c  */
#line 440 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_aliases(&oss);
            oss.close(); CHECK;
       }
    break;

  case 92:

/* Line 1806 of yacc.c  */
#line 445 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_aliases(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 93:

/* Line 1806 of yacc.c  */
#line 448 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_arc_count(&oss);
            oss.close(); CHECK;
       }
    break;

  case 94:

/* Line 1806 of yacc.c  */
#line 453 "xfst-parser.yy"
    {
            if (strcmp((yyvsp[(2) - (3)].name), "upper") && strcmp((yyvsp[(2) - (3)].name), "lower"))
            {
                hxfsterror("should be upper or lower");
                free((yyvsp[(2) - (3)].name));
                return EXIT_FAILURE;
            }
            hfst::xfst::xfst_->print_arc_count((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 95:

/* Line 1806 of yacc.c  */
#line 463 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_arc_count(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 96:

/* Line 1806 of yacc.c  */
#line 466 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_defined(&oss);
            oss.close(); CHECK;
       }
    break;

  case 97:

/* Line 1806 of yacc.c  */
#line 471 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_defined(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 98:

/* Line 1806 of yacc.c  */
#line 474 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(3) - (4)].file));
            hfst::xfst::xfst_->print_dir((yyvsp[(2) - (4)].name), &oss);
            oss.close();
            free((yyvsp[(3) - (4)].file)); CHECK;
       }
    break;

  case 99:

/* Line 1806 of yacc.c  */
#line 480 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_dir((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 100:

/* Line 1806 of yacc.c  */
#line 484 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_dir("*", &oss);
            oss.close(); CHECK;
       }
    break;

  case 101:

/* Line 1806 of yacc.c  */
#line 489 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_dir("*", &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 102:

/* Line 1806 of yacc.c  */
#line 492 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_file_info(&oss);
            oss.close(); CHECK;
       }
    break;

  case 103:

/* Line 1806 of yacc.c  */
#line 497 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_file_info(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 104:

/* Line 1806 of yacc.c  */
#line 500 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_flags(&oss);
            oss.close(); CHECK;
       }
    break;

  case 105:

/* Line 1806 of yacc.c  */
#line 505 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_flags(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 106:

/* Line 1806 of yacc.c  */
#line 508 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_labels((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 107:

/* Line 1806 of yacc.c  */
#line 512 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_labels(&oss);
            oss.close(); CHECK;
       }
    break;

  case 108:

/* Line 1806 of yacc.c  */
#line 517 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_labels(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 109:

/* Line 1806 of yacc.c  */
#line 520 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_label_count(&oss);
            oss.close(); CHECK;
       }
    break;

  case 110:

/* Line 1806 of yacc.c  */
#line 525 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_label_count(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 111:

/* Line 1806 of yacc.c  */
#line 528 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(3) - (4)].file));
            hfst::xfst::xfst_->print_list((yyvsp[(2) - (4)].name), &oss);
            oss.close();
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 112:

/* Line 1806 of yacc.c  */
#line 534 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_list((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 113:

/* Line 1806 of yacc.c  */
#line 538 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_list(&oss);
            oss.close(); CHECK;
       }
    break;

  case 114:

/* Line 1806 of yacc.c  */
#line 543 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_list(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 115:

/* Line 1806 of yacc.c  */
#line 546 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_longest_string(&oss);
            //hfst::xfst::xfst_fclose(f, $2);
            oss.close();
            CHECK;
       }
    break;

  case 116:

/* Line 1806 of yacc.c  */
#line 554 "xfst-parser.yy"
    {
            //hfst::xfst::xfst_->print_longest_string(&hfst::xfst::xfst_->get_output_stream());
            hfst::xfst::xfst_->print_longest_string(&hfst::xfst::xfst_->get_output_stream());
            CHECK;
       }
    break;

  case 117:

/* Line 1806 of yacc.c  */
#line 559 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_longest_string_size(&oss);
            //hfst::xfst::xfst_fclose(f, $2);
            oss.close();
            CHECK;
       }
    break;

  case 118:

/* Line 1806 of yacc.c  */
#line 567 "xfst-parser.yy"
    {
            //hfst::xfst::xfst_->print_longest_string_size(&hfst::xfst::xfst_->get_output_stream());
            hfst::xfst::xfst_->print_longest_string_size(&hfst::xfst::xfst_->get_output_stream());
            CHECK;
       }
    break;

  case 119:

/* Line 1806 of yacc.c  */
#line 572 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_name(&oss);
            oss.close(); CHECK;
       }
    break;

  case 120:

/* Line 1806 of yacc.c  */
#line 577 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_name(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 121:

/* Line 1806 of yacc.c  */
#line 580 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_shortest_string(&oss);
            //hfst::xfst::xfst_fclose(f, $2);
            oss.close();
            CHECK;
       }
    break;

  case 122:

/* Line 1806 of yacc.c  */
#line 588 "xfst-parser.yy"
    {
            //hfst::xfst::xfst_->print_shortest_string(&hfst::xfst::xfst_->get_output_stream());
            hfst::xfst::xfst_->print_shortest_string(&hfst::xfst::xfst_->get_output_stream());
            CHECK;
       }
    break;

  case 123:

/* Line 1806 of yacc.c  */
#line 593 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_shortest_string_size(&oss);
            //hfst::xfst::xfst_fclose(f, $2);
            oss.close();
            CHECK;
       }
    break;

  case 124:

/* Line 1806 of yacc.c  */
#line 601 "xfst-parser.yy"
    {
            //hfst::xfst::xfst_->print_shortest_string_size(&hfst::xfst::xfst_->get_output_stream());
            hfst::xfst::xfst_->print_shortest_string_size(&hfst::xfst::xfst_->get_output_stream());
            CHECK;
       }
    break;

  case 125:

/* Line 1806 of yacc.c  */
#line 606 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_lower_words((yyvsp[(2) - (4)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (4)].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (4)].name)); free((yyvsp[(3) - (4)].name)); CHECK;
       }
    break;

  case 126:

/* Line 1806 of yacc.c  */
#line 610 "xfst-parser.yy"
    {
            //std::ofstream oss($4, "w");
            std::ofstream oss((yyvsp[(4) - (5)].file));
            hfst::xfst::xfst_->print_lower_words((yyvsp[(2) - (5)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (5)].name)), &oss);
            free((yyvsp[(2) - (5)].name)); free((yyvsp[(3) - (5)].name));
            //hfst::xfst::xfst_fclose(f, $4);
            oss.close();
            CHECK;
       }
    break;

  case 127:

/* Line 1806 of yacc.c  */
#line 619 "xfst-parser.yy"
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (3)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_lower_words(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_lower_words((yyvsp[(2) - (3)].name), 0, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name));
            CHECK;
       }
    break;

  case 128:

/* Line 1806 of yacc.c  */
#line 628 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_lower_words(NULL, 0, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 129:

/* Line 1806 of yacc.c  */
#line 631 "xfst-parser.yy"
    {
            //std::ofstream oss($3);
            std::ofstream oss((yyvsp[(3) - (4)].file));
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (4)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_lower_words(NULL, i, &oss);
            else
              hfst::xfst::xfst_->print_lower_words((yyvsp[(2) - (4)].name), 0, &oss);
            //hfst::xfst::xfst_fclose(f, $3);
            oss.close();
            free((yyvsp[(2) - (4)].name));
            CHECK;
       }
    break;

  case 130:

/* Line 1806 of yacc.c  */
#line 644 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_lower_words(NULL, 0, &oss);
            //hfst::xfst::xfst_fclose(f, $2);
            oss.close();
            CHECK;
       }
    break;

  case 131:

/* Line 1806 of yacc.c  */
#line 652 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_random_lower((yyvsp[(2) - (4)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (4)].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (4)].name)); free((yyvsp[(3) - (4)].name)); CHECK;
       }
    break;

  case 132:

/* Line 1806 of yacc.c  */
#line 656 "xfst-parser.yy"
    {
            //std::ofstream oss($4, "w");
            std::ofstream oss((yyvsp[(4) - (5)].file));
            hfst::xfst::xfst_->print_random_lower((yyvsp[(2) - (5)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (5)].name)), &oss);
            free((yyvsp[(2) - (5)].name)); free((yyvsp[(3) - (5)].name));
            oss.close();
            //hfst::xfst::xfst_fclose(f, $4);
            CHECK;
       }
    break;

  case 133:

/* Line 1806 of yacc.c  */
#line 665 "xfst-parser.yy"
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (3)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_random_lower(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_random_lower((yyvsp[(2) - (3)].name), 15, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name));CHECK;
       }
    break;

  case 134:

/* Line 1806 of yacc.c  */
#line 673 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_random_lower(NULL, 15, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 135:

/* Line 1806 of yacc.c  */
#line 676 "xfst-parser.yy"
    {
            //std::ofstream oss($3);
            std::ofstream oss((yyvsp[(3) - (4)].file));
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (4)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_random_lower(NULL, i, &oss);
            else
              hfst::xfst::xfst_->print_random_lower((yyvsp[(2) - (4)].name), 15, &oss);
            //hfst::xfst::xfst_fclose(f, $3);
            oss.close();
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 136:

/* Line 1806 of yacc.c  */
#line 688 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_random_lower(NULL, 15, &oss);
            //hfst::xfst::xfst_fclose(f, $2);
            oss.close();
            CHECK;
       }
    break;

  case 137:

/* Line 1806 of yacc.c  */
#line 696 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_upper_words((yyvsp[(2) - (4)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (4)].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 138:

/* Line 1806 of yacc.c  */
#line 700 "xfst-parser.yy"
    {
            //std::ofstream oss($4, "w");
            std::ofstream oss((yyvsp[(4) - (5)].file));
            hfst::xfst::xfst_->print_upper_words((yyvsp[(2) - (5)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (5)].name)), &oss);
            free((yyvsp[(2) - (5)].name)); free((yyvsp[(3) - (5)].name));
            //hfst::xfst::xfst_fclose(f, $4);
            oss.close();
            CHECK;
       }
    break;

  case 139:

/* Line 1806 of yacc.c  */
#line 709 "xfst-parser.yy"
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (3)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_upper_words(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_upper_words((yyvsp[(2) - (3)].name), 0, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 140:

/* Line 1806 of yacc.c  */
#line 717 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_upper_words(NULL, 0, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 141:

/* Line 1806 of yacc.c  */
#line 720 "xfst-parser.yy"
    {
            //std::ofstream oss($3);
            std::ofstream oss((yyvsp[(3) - (4)].file));
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (4)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_upper_words(NULL, i, &oss);
            else
              hfst::xfst::xfst_->print_upper_words((yyvsp[(2) - (4)].name), 0, &oss);
            //hfst::xfst::xfst_fclose(f, $3);
            oss.close();
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 142:

/* Line 1806 of yacc.c  */
#line 732 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_upper_words(NULL, 0, &oss);
            //hfst::xfst::xfst_fclose(f, $2);
            oss.close();
            CHECK;
       }
    break;

  case 143:

/* Line 1806 of yacc.c  */
#line 740 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_random_upper((yyvsp[(2) - (4)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (4)].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (4)].name)); free((yyvsp[(3) - (4)].name)); CHECK;
       }
    break;

  case 144:

/* Line 1806 of yacc.c  */
#line 744 "xfst-parser.yy"
    {
            //std::ofstream oss($4, "w");
            std::ofstream oss((yyvsp[(4) - (5)].file));
            hfst::xfst::xfst_->print_random_upper((yyvsp[(2) - (5)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (5)].name)), &oss);
            free((yyvsp[(2) - (5)].name)); free((yyvsp[(3) - (5)].name));
            //hfst::xfst::xfst_fclose(f, $4);
            oss.close();
            CHECK;
       }
    break;

  case 145:

/* Line 1806 of yacc.c  */
#line 753 "xfst-parser.yy"
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (3)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_random_upper(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_random_upper((yyvsp[(2) - (3)].name), 15, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 146:

/* Line 1806 of yacc.c  */
#line 761 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_random_upper(NULL, 15, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 147:

/* Line 1806 of yacc.c  */
#line 764 "xfst-parser.yy"
    {
            //std::ofstream oss($3);
            std::ofstream oss((yyvsp[(3) - (4)].file));
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (4)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_random_upper(NULL, i, &oss);
            else
              hfst::xfst::xfst_->print_random_upper((yyvsp[(2) - (4)].name), 15, &oss);
            //hfst::xfst::xfst_fclose(f, $3);
            oss.close();
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 148:

/* Line 1806 of yacc.c  */
#line 776 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_random_upper(NULL, 15, &oss);
            //hfst::xfst::xfst_fclose(f, $2);
            oss.close();
            CHECK;
       }
    break;

  case 149:

/* Line 1806 of yacc.c  */
#line 784 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_words((yyvsp[(2) - (4)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (4)].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (4)].name)); free((yyvsp[(3) - (4)].name)); CHECK;
       }
    break;

  case 150:

/* Line 1806 of yacc.c  */
#line 788 "xfst-parser.yy"
    {
            //std::ofstream oss($4, "w");
            std::ofstream oss((yyvsp[(4) - (5)].file));
            hfst::xfst::xfst_->print_words((yyvsp[(2) - (5)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (5)].name)), &oss);
            free((yyvsp[(2) - (5)].name)); free((yyvsp[(3) - (5)].name));
            //hfst::xfst::xfst_fclose(f, $4);
            oss.close();
            CHECK;
       }
    break;

  case 151:

/* Line 1806 of yacc.c  */
#line 797 "xfst-parser.yy"
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (3)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_words(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_words((yyvsp[(2) - (3)].name), 0, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 152:

/* Line 1806 of yacc.c  */
#line 805 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_words(NULL, 0, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 153:

/* Line 1806 of yacc.c  */
#line 808 "xfst-parser.yy"
    {
            //std::ofstream oss($3);
            std::ofstream oss((yyvsp[(3) - (4)].file));
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (4)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_words(NULL, i, &oss);
            else
              hfst::xfst::xfst_->print_words((yyvsp[(2) - (4)].name), 0, &oss);
            //hfst::xfst::xfst_fclose(f, $3);
            oss.close();
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 154:

/* Line 1806 of yacc.c  */
#line 820 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_words(NULL, 0, &oss);
            oss.close();
            //hfst::xfst::xfst_fclose(f, $2);
            CHECK;
       }
    break;

  case 155:

/* Line 1806 of yacc.c  */
#line 828 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_random_words((yyvsp[(2) - (4)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (4)].name)), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (4)].name)); free((yyvsp[(3) - (4)].name)); CHECK;
       }
    break;

  case 156:

/* Line 1806 of yacc.c  */
#line 832 "xfst-parser.yy"
    {
            //std::ofstream oss($4, "w");
            std::ofstream oss((yyvsp[(4) - (5)].file));
            hfst::xfst::xfst_->print_random_words((yyvsp[(2) - (5)].name), hfst::xfst::nametoken_to_number((yyvsp[(3) - (5)].name)), &oss);
            free((yyvsp[(2) - (5)].name)); free((yyvsp[(3) - (5)].name));
            //hfst::xfst::xfst_fclose(f, $4);
            oss.close();
            CHECK;
       }
    break;

  case 157:

/* Line 1806 of yacc.c  */
#line 841 "xfst-parser.yy"
    {
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (3)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_random_words(NULL, i, &hfst::xfst::xfst_->get_output_stream());
            else
              hfst::xfst::xfst_->print_random_words((yyvsp[(2) - (3)].name), 15, &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 158:

/* Line 1806 of yacc.c  */
#line 849 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_random_words(NULL, 15, &hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 159:

/* Line 1806 of yacc.c  */
#line 852 "xfst-parser.yy"
    {
            //std::ofstream oss($3);
            std::ofstream oss((yyvsp[(3) - (4)].file));
            int i = hfst::xfst::nametoken_to_number((yyvsp[(2) - (4)].name));
            if (i != -1)
              hfst::xfst::xfst_->print_random_words(NULL, i, &oss);
            else
              hfst::xfst::xfst_->print_random_words((yyvsp[(2) - (4)].name), 15, &oss);
            //hfst::xfst::xfst_fclose(f, $3);
            oss.close();
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 160:

/* Line 1806 of yacc.c  */
#line 864 "xfst-parser.yy"
    {
            //std::ofstream oss($2);
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_random_words(NULL, 15, &oss);
            //hfst::xfst::xfst_fclose(f, $2);
            oss.close();
            CHECK;
       }
    break;

  case 161:

/* Line 1806 of yacc.c  */
#line 872 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_net((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 162:

/* Line 1806 of yacc.c  */
#line 876 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_net(&oss);
            oss.close(); CHECK;
       }
    break;

  case 163:

/* Line 1806 of yacc.c  */
#line 881 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_net(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 164:

/* Line 1806 of yacc.c  */
#line 884 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_properties((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 165:

/* Line 1806 of yacc.c  */
#line 888 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_properties(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 166:

/* Line 1806 of yacc.c  */
#line 891 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_properties(&oss);
            oss.close(); CHECK;
       }
    break;

  case 167:

/* Line 1806 of yacc.c  */
#line 896 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_sigma((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 168:

/* Line 1806 of yacc.c  */
#line 900 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_sigma(&oss);
            oss.close(); CHECK;
       }
    break;

  case 169:

/* Line 1806 of yacc.c  */
#line 905 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_sigma(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 170:

/* Line 1806 of yacc.c  */
#line 908 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_sigma_count(&oss);
            oss.close(); CHECK;
       }
    break;

  case 171:

/* Line 1806 of yacc.c  */
#line 913 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_sigma_count(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 172:

/* Line 1806 of yacc.c  */
#line 916 "xfst-parser.yy"
    {
            if (strcmp((yyvsp[(2) - (3)].name), "upper") && strcmp((yyvsp[(2) - (3)].name), "lower"))
            {
                free((yyvsp[(2) - (3)].name));
                hxfsterror("must be upper or lower\n");
                return EXIT_FAILURE;
            }
            hfst::xfst::xfst_->print_sigma_word_count((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 173:

/* Line 1806 of yacc.c  */
#line 926 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_sigma_word_count(&oss);
            oss.close(); CHECK;
       }
    break;

  case 174:

/* Line 1806 of yacc.c  */
#line 931 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_sigma_word_count(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 175:

/* Line 1806 of yacc.c  */
#line 934 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_size((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 176:

/* Line 1806 of yacc.c  */
#line 938 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_size(&oss);
            oss.close(); CHECK;
       }
    break;

  case 177:

/* Line 1806 of yacc.c  */
#line 943 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_size(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 178:

/* Line 1806 of yacc.c  */
#line 946 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_stack(&oss);
            oss.close(); CHECK;
       }
    break;

  case 179:

/* Line 1806 of yacc.c  */
#line 951 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->print_stack(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 180:

/* Line 1806 of yacc.c  */
#line 954 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->print_labelmaps(&oss);
            oss.close(); CHECK;
       }
    break;

  case 181:

/* Line 1806 of yacc.c  */
#line 960 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_dot((yyvsp[(2) - (3)].name), &hfst::xfst::xfst_->get_output_stream());
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 182:

/* Line 1806 of yacc.c  */
#line 964 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->write_dot(&oss);
            oss.close(); CHECK;
       }
    break;

  case 183:

/* Line 1806 of yacc.c  */
#line 969 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_dot(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 184:

/* Line 1806 of yacc.c  */
#line 972 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_function((yyvsp[(2) - (5)].name), (yyvsp[(4) - (5)].file));
            free((yyvsp[(2) - (5)].name)); CHECK;
       }
    break;

  case 185:

/* Line 1806 of yacc.c  */
#line 976 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_function((yyvsp[(2) - (4)].name), 0);
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 186:

/* Line 1806 of yacc.c  */
#line 980 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_definition((yyvsp[(2) - (4)].name), (yyvsp[(3) - (4)].file));
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 187:

/* Line 1806 of yacc.c  */
#line 984 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_definition((yyvsp[(2) - (3)].name), 0);
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 188:

/* Line 1806 of yacc.c  */
#line 988 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_definitions((yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 189:

/* Line 1806 of yacc.c  */
#line 991 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_definitions(0); CHECK;
       }
    break;

  case 190:

/* Line 1806 of yacc.c  */
#line 994 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_stack((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 191:

/* Line 1806 of yacc.c  */
#line 998 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->write_prolog(&oss);
            oss.close(); CHECK;
       }
    break;

  case 192:

/* Line 1806 of yacc.c  */
#line 1003 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].name));
            hfst::xfst::xfst_->write_prolog(&oss);
            oss.close(); free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 193:

/* Line 1806 of yacc.c  */
#line 1008 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_prolog(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 194:

/* Line 1806 of yacc.c  */
#line 1011 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->write_spaced(&oss);
            oss.close(); CHECK;
       }
    break;

  case 195:

/* Line 1806 of yacc.c  */
#line 1016 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_spaced(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 196:

/* Line 1806 of yacc.c  */
#line 1019 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->write_text(&oss);
            oss.close(); CHECK;
       }
    break;

  case 197:

/* Line 1806 of yacc.c  */
#line 1024 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_text(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 198:

/* Line 1806 of yacc.c  */
#line 1028 "xfst-parser.yy"
    {
            FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[(2) - (3)].file), "r"); CHECK;
            hfst::xfst::xfst_->read_props(f);
            hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 199:

/* Line 1806 of yacc.c  */
#line 1033 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_props(stdin); CHECK;
       }
    break;

  case 200:

/* Line 1806 of yacc.c  */
#line 1036 "xfst-parser.yy"
    {
            FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[(2) - (3)].name), "r"); CHECK;
            hfst::xfst::xfst_->read_prolog(f);
            hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[(2) - (3)].name)); free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 201:

/* Line 1806 of yacc.c  */
#line 1041 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_prolog(stdin); CHECK;
       }
    break;

  case 202:

/* Line 1806 of yacc.c  */
#line 1044 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_regex((yyvsp[(2) - (2)].text));
            free((yyvsp[(2) - (2)].text)); CHECK;
       }
    break;

  case 203:

/* Line 1806 of yacc.c  */
#line 1048 "xfst-parser.yy"
    {
            FILE * f = hfst::xfst::xfst_->xfst_fopen((yyvsp[(2) - (3)].file), "r"); CHECK;
            hfst::xfst::xfst_->read_regex(f);
            hfst::xfst::xfst_->xfst_fclose(f, (yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 204:

/* Line 1806 of yacc.c  */
#line 1053 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_regex((yyvsp[(2) - (4)].text));
            free((yyvsp[(2) - (4)].text)); CHECK;
       }
    break;

  case 205:

/* Line 1806 of yacc.c  */
#line 1057 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_spaced_from_file((yyvsp[(2) - (3)].file));
            free((yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 206:

/* Line 1806 of yacc.c  */
#line 1061 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_spaced_from_file((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 207:

/* Line 1806 of yacc.c  */
#line 1065 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_spaced((yyvsp[(2) - (3)].text));
            free((yyvsp[(2) - (3)].text)); CHECK;
       }
    break;

  case 208:

/* Line 1806 of yacc.c  */
#line 1069 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_text_from_file((yyvsp[(2) - (3)].file));
            free((yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 209:

/* Line 1806 of yacc.c  */
#line 1073 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_text_from_file((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 210:

/* Line 1806 of yacc.c  */
#line 1077 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_text((yyvsp[(2) - (3)].text));
            free((yyvsp[(2) - (3)].text)); CHECK;
       }
    break;

  case 211:

/* Line 1806 of yacc.c  */
#line 1081 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_lexc_from_file((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 212:

/* Line 1806 of yacc.c  */
#line 1085 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_lexc_from_file((yyvsp[(2) - (4)].name));
            free((yyvsp[(2) - (4)].name)); CHECK;
       }
    break;

  case 213:

/* Line 1806 of yacc.c  */
#line 1089 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_lexc_from_file(""); free((yyvsp[(2) - (3)].text)); CHECK;
       }
    break;

  case 214:

/* Line 1806 of yacc.c  */
#line 1092 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->read_att_from_file((yyvsp[(2) - (3)].name));
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 215:

/* Line 1806 of yacc.c  */
#line 1096 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->write_att(&hfst::xfst::xfst_->get_output_stream()); CHECK;
       }
    break;

  case 216:

/* Line 1806 of yacc.c  */
#line 1099 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].file));
            hfst::xfst::xfst_->write_att(&oss);
            oss.close();
            free((yyvsp[(2) - (3)].file)); CHECK;
       }
    break;

  case 217:

/* Line 1806 of yacc.c  */
#line 1105 "xfst-parser.yy"
    {
            std::ofstream oss((yyvsp[(2) - (3)].name));
            hfst::xfst::xfst_->write_att(&oss);
            oss.close();
            free((yyvsp[(2) - (3)].name)); CHECK;
       }
    break;

  case 218:

/* Line 1806 of yacc.c  */
#line 1111 "xfst-parser.yy"
    {
            // todo: handle input and output symbol tables
            std::ofstream oss((yyvsp[(2) - (5)].name));
            hfst::xfst::xfst_->write_att(&oss);
            oss.close();
            free((yyvsp[(2) - (5)].name)); free((yyvsp[(3) - (5)].name)); free((yyvsp[(4) - (5)].name)); CHECK;
       }
    break;

  case 219:

/* Line 1806 of yacc.c  */
#line 1119 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->cleanup_net(); CHECK;
       }
    break;

  case 220:

/* Line 1806 of yacc.c  */
#line 1122 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->complete_net(); CHECK;
       }
    break;

  case 221:

/* Line 1806 of yacc.c  */
#line 1125 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->compose_net(); CHECK;
       }
    break;

  case 222:

/* Line 1806 of yacc.c  */
#line 1128 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->concatenate_net(); CHECK;
       }
    break;

  case 223:

/* Line 1806 of yacc.c  */
#line 1131 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->minus_net(); CHECK;
       }
    break;

  case 224:

/* Line 1806 of yacc.c  */
#line 1134 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->crossproduct_net(); CHECK;
       }
    break;

  case 225:

/* Line 1806 of yacc.c  */
#line 1137 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->minimize_net(); CHECK;
       }
    break;

  case 226:

/* Line 1806 of yacc.c  */
#line 1140 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->determinize_net(); CHECK;
       }
    break;

  case 227:

/* Line 1806 of yacc.c  */
#line 1143 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->epsilon_remove_net(); CHECK;
       }
    break;

  case 228:

/* Line 1806 of yacc.c  */
#line 1146 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->prune_net(); CHECK;
       }
    break;

  case 229:

/* Line 1806 of yacc.c  */
#line 1149 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->ignore_net(); CHECK;
       }
    break;

  case 230:

/* Line 1806 of yacc.c  */
#line 1152 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->intersect_net(); CHECK;
       }
    break;

  case 231:

/* Line 1806 of yacc.c  */
#line 1155 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->inspect_net(); CHECK;
       }
    break;

  case 232:

/* Line 1806 of yacc.c  */
#line 1158 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->invert_net(); CHECK;
       }
    break;

  case 233:

/* Line 1806 of yacc.c  */
#line 1161 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->lower_side_net(); CHECK;
       }
    break;

  case 234:

/* Line 1806 of yacc.c  */
#line 1164 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->upper_side_net(); CHECK;
       }
    break;

  case 235:

/* Line 1806 of yacc.c  */
#line 1167 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->negate_net(); CHECK;
       }
    break;

  case 236:

/* Line 1806 of yacc.c  */
#line 1170 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->one_plus_net(); CHECK;
       }
    break;

  case 237:

/* Line 1806 of yacc.c  */
#line 1173 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->zero_plus_net(); CHECK;
       }
    break;

  case 238:

/* Line 1806 of yacc.c  */
#line 1176 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->optional_net(); CHECK;
       }
    break;

  case 239:

/* Line 1806 of yacc.c  */
#line 1179 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->reverse_net(); CHECK;
       }
    break;

  case 240:

/* Line 1806 of yacc.c  */
#line 1182 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->shuffle_net(); CHECK;
       }
    break;

  case 241:

/* Line 1806 of yacc.c  */
#line 1185 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->sigma_net(); CHECK;
       }
    break;

  case 242:

/* Line 1806 of yacc.c  */
#line 1188 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->sort_net(); CHECK;
       }
    break;

  case 243:

/* Line 1806 of yacc.c  */
#line 1191 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->substring_net(); CHECK;
       }
    break;

  case 244:

/* Line 1806 of yacc.c  */
#line 1194 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->union_net(); CHECK;
       }
    break;

  case 245:

/* Line 1806 of yacc.c  */
#line 1197 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->label_net(); CHECK;
       }
    break;

  case 246:

/* Line 1806 of yacc.c  */
#line 1200 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->compile_replace_lower_net(); CHECK;
       }
    break;

  case 247:

/* Line 1806 of yacc.c  */
#line 1203 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->compile_replace_upper_net(); CHECK;
       }
    break;

  case 248:

/* Line 1806 of yacc.c  */
#line 1206 "xfst-parser.yy"
    {
            hfst::xfst::xfst_->prompt(); CHECK;
       }
    break;

  case 249:

/* Line 1806 of yacc.c  */
#line 1209 "xfst-parser.yy"
    {
            if ( hfst::xfst::xfst_->unknown_command((yyvsp[(1) - (2)].name)) != 0)
              {
                hxfsterror("Command not recognized.\n");
                free((yyvsp[(1) - (2)].name));
                YYABORT;
              }
            free((yyvsp[(1) - (2)].name));
       }
    break;

  case 252:

/* Line 1806 of yacc.c  */
#line 1222 "xfst-parser.yy"
    {
                    (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[(1) - (2)].text))+strlen((yyvsp[(2) - (2)].name))+2));
                    char* r = (yyval.text);
                    char* s = (yyvsp[(1) - (2)].text);
                    while (*s != '\0')
                    {
                        *r = *s;
                        r++;
                        s++;
                    }
                    *r = ' ';
                    r++;
                    s = (yyvsp[(2) - (2)].name);
                    while (*s != '\0')
                    {
                        *r = *s;
                        r++;
                        s++;
                    }
                    *r = '\0';
                    free((yyvsp[(2) - (2)].name));
                }
    break;

  case 253:

/* Line 1806 of yacc.c  */
#line 1244 "xfst-parser.yy"
    {
                    (yyval.text) = (yyvsp[(1) - (2)].text);
                }
    break;

  case 254:

/* Line 1806 of yacc.c  */
#line 1247 "xfst-parser.yy"
    {
                    (yyval.text) = (yyvsp[(1) - (1)].name);
                }
    break;

  case 255:

/* Line 1806 of yacc.c  */
#line 1252 "xfst-parser.yy"
    {
                (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[(1) - (2)].text))+strlen((yyvsp[(2) - (2)].name))+2));
                char* s = (yyvsp[(1) - (2)].text);
                char* r = (yyval.text);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = ' ';
                r++;
                s = (yyvsp[(2) - (2)].name);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = '\0';
                free((yyvsp[(1) - (2)].text)); free((yyvsp[(2) - (2)].name));
             }
    break;

  case 256:

/* Line 1806 of yacc.c  */
#line 1274 "xfst-parser.yy"
    {
                (yyval.text) = (yyvsp[(1) - (1)].name);
             }
    break;

  case 257:

/* Line 1806 of yacc.c  */
#line 1279 "xfst-parser.yy"
    {
                (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[(1) - (2)].text))+strlen((yyvsp[(2) - (2)].name))+4));
                char* s = (yyvsp[(1) - (2)].text);
                char* r = (yyval.text);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = ' ';
                r++;
                s = (yyvsp[(2) - (2)].name);
                *r = '"';
                r++;
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = '"';
                r++;
                *r = '\0';
                free((yyvsp[(1) - (2)].text)); free((yyvsp[(2) - (2)].name));
             }
    break;

  case 258:

/* Line 1806 of yacc.c  */
#line 1305 "xfst-parser.yy"
    {
                (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[(1) - (1)].name))+3));
                char* s = (yyvsp[(1) - (1)].name);
                char* r = (yyval.text);
                *r = '"';
                r++;
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = '"';
                r++;
                *r = '\0';
                free((yyvsp[(1) - (1)].name));
             }
    break;

  case 259:

/* Line 1806 of yacc.c  */
#line 1324 "xfst-parser.yy"
    {
                (yyval.text) = strdup((std::string((yyvsp[(1) - (3)].name)) + std::string(":") + std::string((yyvsp[(3) - (3)].name))).c_str());
                free((yyvsp[(1) - (3)].name)); free((yyvsp[(3) - (3)].name));
                }
    break;

  case 260:

/* Line 1806 of yacc.c  */
#line 1328 "xfst-parser.yy"
    {
                (yyval.text) = (yyvsp[(1) - (1)].name);
                }
    break;

  case 261:

/* Line 1806 of yacc.c  */
#line 1333 "xfst-parser.yy"
    {
                (yyval.text) = static_cast<char*>(malloc(sizeof(char)*strlen((yyvsp[(1) - (2)].text))+strlen((yyvsp[(2) - (2)].text))+2));
                char* s = (yyvsp[(1) - (2)].text);
                char* r = (yyval.text);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = ' ';
                r++;
                s = (yyvsp[(2) - (2)].text);
                while (*s != '\0')
                {
                    *r = *s;
                    r++;
                    s++;
                }
                *r = '\0';
                free((yyvsp[(1) - (2)].text)); free((yyvsp[(2) - (2)].text));
             }
    break;

  case 262:

/* Line 1806 of yacc.c  */
#line 1355 "xfst-parser.yy"
    {
                (yyval.text) = (yyvsp[(1) - (1)].text);
             }
    break;



/* Line 1806 of yacc.c  */
#line 5111 "xfst-parser.cc"
      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;
  *++yylsp = yyloc;

  /* Now `shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*------------------------------------.
| yyerrlab -- here on detecting error |
`------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = (char *) YYSTACK_ALLOC (yymsg_alloc);
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }

  yyerror_range[1] = yylloc;

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
	 error, discard it.  */

      if (yychar <= YYEOF)
	{
	  /* Return failure if at end of input.  */
	  if (yychar == YYEOF)
	    YYABORT;
	}
      else
	{
	  yydestruct ("Error: discarding",
		      yytoken, &yylval, &yylloc);
	  yychar = YYEMPTY;
	}
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  yyerror_range[1] = yylsp[1-yylen];
  /* Do not reclaim the symbols of the rule which action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;	/* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
	{
	  yyn += YYTERROR;
	  if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
	    {
	      yyn = yytable[yyn];
	      if (0 < yyn)
		break;
	    }
	}

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
	YYABORT;

      yyerror_range[1] = *yylsp;
      yydestruct ("Error: popping",
		  yystos[yystate], yyvsp, yylsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  *++yyvsp = yylval;

  yyerror_range[2] = yylloc;
  /* Using YYLLOC is tempting, but would change the location of
     the lookahead.  YYLOC is available though.  */
  YYLLOC_DEFAULT (yyloc, yyerror_range, 2);
  *++yylsp = yyloc;

  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined(yyoverflow) || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval, &yylloc);
    }
  /* Do not reclaim the symbols of the rule which action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
		  yystos[*yyssp], yyvsp, yylsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  /* Make sure YYID is used.  */
  return YYID (yyresult);
}



/* Line 2067 of yacc.c  */
#line 1359 "xfst-parser.yy"


// oblig. declarations
extern FILE* hxfstin;
int hxfstparse(void);

// gah, bison/flex error mechanism here
void
hxfsterror(const char* text)
{
    hfst::xfst::xfst_->error() << text << std::endl;
    hfst::xfst::xfst_->flush(&hfst::xfst::xfst_->error());
    //fprintf(stderr,  "%s\n", text);
}


// vim: set ft=yacc:

