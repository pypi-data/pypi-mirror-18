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
#define YYLSP_NEEDED 0

/* Substitute the variable and function names.  */
#define yyparse         pmatchparse
#define yylex           pmatchlex
#define yyerror         pmatcherror
#define yylval          pmatchlval
#define yychar          pmatchchar
#define yydebug         pmatchdebug
#define yynerrs         pmatchnerrs


/* Copy the first part of user declarations.  */

/* Line 268 of yacc.c  */
#line 1 "pmatch_parse.yy"

// Copyright (c) 2016 University of Helsinki
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 3 of the License, or (at your option) any later version.
// See the file COPYING included with this distribution for more
// information.

#define YYDEBUG 0

#include <stdio.h>
#include <assert.h>
#include <iostream>
#include <sstream>
    
#include "HfstTransducer.h"
#include "HfstInputStream.h"
#include "HfstXeroxRules.h"
    
#include "pmatch_utils.h"
    using namespace hfst;
    using namespace hfst::pmatch;
    using namespace hfst::xeroxRules;

    extern int pmatcherror(const char * text);
    extern int pmatchlex();
    extern int pmatchlineno;

    

/* Line 268 of yacc.c  */
#line 112 "pmatch_parse.cc"

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
     WEIGHT = 258,
     END_OF_WEIGHTED_EXPRESSION = 259,
     CHARACTER_RANGE = 260,
     MERGE_LEFT_ARROW = 261,
     MERGE_RIGHT_ARROW = 262,
     INTERSECTION = 263,
     LENIENT_COMPOSITION = 264,
     COMPOSITION = 265,
     CROSS_PRODUCT = 266,
     MARKUP_MARKER = 267,
     CENTER_MARKER = 268,
     AFTER = 269,
     BEFORE = 270,
     SHUFFLE = 271,
     LEFT_RESTRICTION = 272,
     LEFT_RIGHT_ARROW = 273,
     RIGHT_ARROW = 274,
     LEFT_ARROW = 275,
     LTR_SHORTEST_MATCH = 276,
     LTR_LONGEST_MATCH = 277,
     RTL_SHORTEST_MATCH = 278,
     RTL_LONGEST_MATCH = 279,
     OPTIONAL_REPLACE_LEFT_RIGHT = 280,
     REPLACE_LEFT_RIGHT = 281,
     OPTIONAL_REPLACE_LEFT = 282,
     OPTIONAL_REPLACE_RIGHT = 283,
     REPLACE_LEFT = 284,
     REPLACE_RIGHT = 285,
     REPLACE_CONTEXT_LL = 286,
     REPLACE_CONTEXT_UL = 287,
     REPLACE_CONTEXT_LU = 288,
     REPLACE_CONTEXT_UU = 289,
     LOWER_PRIORITY_UNION = 290,
     UPPER_PRIORITY_UNION = 291,
     LOWER_MINUS = 292,
     UPPER_MINUS = 293,
     MINUS = 294,
     UNION = 295,
     LEFT_QUOTIENT = 296,
     IGNORE_INTERNALLY = 297,
     IGNORING = 298,
     COMMACOMMA = 299,
     COMMA = 300,
     CONTAINMENT_OPT = 301,
     CONTAINMENT_ONCE = 302,
     CONTAINMENT = 303,
     COMPLEMENT = 304,
     TERM_COMPLEMENT = 305,
     SUBSTITUTE_LEFT = 306,
     LOWER_PROJECT = 307,
     UPPER_PROJECT = 308,
     INVERT = 309,
     REVERSE = 310,
     PLUS = 311,
     STAR = 312,
     READ_LEXC = 313,
     READ_VEC = 314,
     READ_RE = 315,
     READ_PROLOG = 316,
     READ_SPACED = 317,
     READ_TEXT = 318,
     READ_BIN = 319,
     CATENATE_N_TO_K = 320,
     CATENATE_N_MINUS = 321,
     CATENATE_N_PLUS = 322,
     CATENATE_N = 323,
     LEFT_BRACKET = 324,
     RIGHT_BRACKET = 325,
     LEFT_PARENTHESIS = 326,
     RIGHT_PARENTHESIS = 327,
     LEFT_BRACKET_DOTTED = 328,
     RIGHT_BRACKET_DOTTED = 329,
     PAIR_SEPARATOR = 330,
     PAIR_SEPARATOR_SOLE = 331,
     PAIR_SEPARATOR_WO_RIGHT = 332,
     PAIR_SEPARATOR_WO_LEFT = 333,
     EPSILON_TOKEN = 334,
     ANY_TOKEN = 335,
     BOUNDARY_MARKER = 336,
     LEXER_ERROR = 337,
     SYMBOL = 338,
     SYMBOL_WITH_LEFT_PAREN = 339,
     QUOTED_LITERAL = 340,
     CURLY_LITERAL = 341,
     ALPHA = 342,
     LOWERALPHA = 343,
     UPPERALPHA = 344,
     NUM = 345,
     PUNCT = 346,
     WHITESPACE = 347,
     VARIABLE_NAME = 348,
     COUNTER_LEFT = 349,
     SIGMA_LEFT = 350,
     INTERPOLATE_LEFT = 351,
     EXC_LEFT = 352,
     LST_LEFT = 353,
     TAG_LEFT = 354,
     AND_LEFT = 355,
     OR_LEFT = 356,
     NRC_LEFT = 357,
     NLC_LEFT = 358,
     RC_LEFT = 359,
     LC_LEFT = 360,
     LIKE_LEFT = 361,
     ENDTAG_LEFT = 362,
     DEFINE_LEFT = 363,
     EXPLODE_LEFT = 364,
     IMPLODE_LEFT = 365,
     ANY_CASE_LEFT = 366,
     TOUPPER_LEFT = 367,
     OPT_TOUPPER_LEFT = 368,
     TOLOWER_LEFT = 369,
     OPT_TOLOWER_LEFT = 370,
     OPTCAP_LEFT = 371,
     CAP_LEFT = 372,
     DEFINED_LIST = 373,
     DEFINS = 374,
     REGEX = 375,
     INS_LEFT = 376,
     LIT_LEFT = 377,
     SET_VARIABLE = 378,
     DEFINE = 379
   };
#endif
/* Tokens.  */
#define WEIGHT 258
#define END_OF_WEIGHTED_EXPRESSION 259
#define CHARACTER_RANGE 260
#define MERGE_LEFT_ARROW 261
#define MERGE_RIGHT_ARROW 262
#define INTERSECTION 263
#define LENIENT_COMPOSITION 264
#define COMPOSITION 265
#define CROSS_PRODUCT 266
#define MARKUP_MARKER 267
#define CENTER_MARKER 268
#define AFTER 269
#define BEFORE 270
#define SHUFFLE 271
#define LEFT_RESTRICTION 272
#define LEFT_RIGHT_ARROW 273
#define RIGHT_ARROW 274
#define LEFT_ARROW 275
#define LTR_SHORTEST_MATCH 276
#define LTR_LONGEST_MATCH 277
#define RTL_SHORTEST_MATCH 278
#define RTL_LONGEST_MATCH 279
#define OPTIONAL_REPLACE_LEFT_RIGHT 280
#define REPLACE_LEFT_RIGHT 281
#define OPTIONAL_REPLACE_LEFT 282
#define OPTIONAL_REPLACE_RIGHT 283
#define REPLACE_LEFT 284
#define REPLACE_RIGHT 285
#define REPLACE_CONTEXT_LL 286
#define REPLACE_CONTEXT_UL 287
#define REPLACE_CONTEXT_LU 288
#define REPLACE_CONTEXT_UU 289
#define LOWER_PRIORITY_UNION 290
#define UPPER_PRIORITY_UNION 291
#define LOWER_MINUS 292
#define UPPER_MINUS 293
#define MINUS 294
#define UNION 295
#define LEFT_QUOTIENT 296
#define IGNORE_INTERNALLY 297
#define IGNORING 298
#define COMMACOMMA 299
#define COMMA 300
#define CONTAINMENT_OPT 301
#define CONTAINMENT_ONCE 302
#define CONTAINMENT 303
#define COMPLEMENT 304
#define TERM_COMPLEMENT 305
#define SUBSTITUTE_LEFT 306
#define LOWER_PROJECT 307
#define UPPER_PROJECT 308
#define INVERT 309
#define REVERSE 310
#define PLUS 311
#define STAR 312
#define READ_LEXC 313
#define READ_VEC 314
#define READ_RE 315
#define READ_PROLOG 316
#define READ_SPACED 317
#define READ_TEXT 318
#define READ_BIN 319
#define CATENATE_N_TO_K 320
#define CATENATE_N_MINUS 321
#define CATENATE_N_PLUS 322
#define CATENATE_N 323
#define LEFT_BRACKET 324
#define RIGHT_BRACKET 325
#define LEFT_PARENTHESIS 326
#define RIGHT_PARENTHESIS 327
#define LEFT_BRACKET_DOTTED 328
#define RIGHT_BRACKET_DOTTED 329
#define PAIR_SEPARATOR 330
#define PAIR_SEPARATOR_SOLE 331
#define PAIR_SEPARATOR_WO_RIGHT 332
#define PAIR_SEPARATOR_WO_LEFT 333
#define EPSILON_TOKEN 334
#define ANY_TOKEN 335
#define BOUNDARY_MARKER 336
#define LEXER_ERROR 337
#define SYMBOL 338
#define SYMBOL_WITH_LEFT_PAREN 339
#define QUOTED_LITERAL 340
#define CURLY_LITERAL 341
#define ALPHA 342
#define LOWERALPHA 343
#define UPPERALPHA 344
#define NUM 345
#define PUNCT 346
#define WHITESPACE 347
#define VARIABLE_NAME 348
#define COUNTER_LEFT 349
#define SIGMA_LEFT 350
#define INTERPOLATE_LEFT 351
#define EXC_LEFT 352
#define LST_LEFT 353
#define TAG_LEFT 354
#define AND_LEFT 355
#define OR_LEFT 356
#define NRC_LEFT 357
#define NLC_LEFT 358
#define RC_LEFT 359
#define LC_LEFT 360
#define LIKE_LEFT 361
#define ENDTAG_LEFT 362
#define DEFINE_LEFT 363
#define EXPLODE_LEFT 364
#define IMPLODE_LEFT 365
#define ANY_CASE_LEFT 366
#define TOUPPER_LEFT 367
#define OPT_TOUPPER_LEFT 368
#define TOLOWER_LEFT 369
#define OPT_TOLOWER_LEFT 370
#define OPTCAP_LEFT 371
#define CAP_LEFT 372
#define DEFINED_LIST 373
#define DEFINS 374
#define REGEX 375
#define INS_LEFT 376
#define LIT_LEFT 377
#define SET_VARIABLE 378
#define DEFINE 379




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 293 of yacc.c  */
#line 36 "pmatch_parse.yy"

         int value;
         int* values;
         double weight;
         char* label;
         hfst::pmatch::PmatchObject* pmatchObject;
         std::pair<std::string, hfst::pmatch::PmatchObject*>* pmatchDefinition;
         std::vector<hfst::pmatch::PmatchObject *>* pmatchObject_vector;
         std::vector<std::string>* string_vector;

         hfst::pmatch::PmatchParallelRulesContainer * replaceRules;
         hfst::pmatch::PmatchReplaceRuleContainer * replaceRule;
         hfst::pmatch::PmatchMappingPairsContainer * mappings;
         hfst::pmatch::PmatchContextsContainer * parallelContexts;
         hfst::pmatch::PmatchObjectPair * restrictionContext;
         hfst::pmatch::MappingPairVector * restrictionContexts;
         hfst::xeroxRules::ReplaceType replType;
         hfst::xeroxRules::ReplaceArrow replaceArrow;
     


/* Line 293 of yacc.c  */
#line 418 "pmatch_parse.cc"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif


/* Copy the second part of user declarations.  */


/* Line 343 of yacc.c  */
#line 430 "pmatch_parse.cc"

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
	 || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

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
#define YYFINAL  2
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   1325

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  125
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  46
/* YYNRULES -- Number of rules.  */
#define YYNRULES  191
/* YYNRULES -- Number of states.  */
#define YYNSTATES  339

/* YYTRANSLATE(YYLEX) -- Bison symbol number corresponding to YYLEX.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   379

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
     115,   116,   117,   118,   119,   120,   121,   122,   123,   124
};

#if YYDEBUG
/* YYPRHS[YYN] -- Index of the first RHS symbol of rule number YYN in
   YYRHS.  */
static const yytype_uint16 yyprhs[] =
{
       0,     0,     3,     4,     7,    12,    17,    20,    24,    28,
      31,    37,    41,    45,    49,    51,    53,    54,    57,    59,
      63,    67,    71,    75,    79,    88,    91,    94,    96,    98,
     100,   104,   106,   108,   111,   115,   117,   121,   127,   132,
     137,   142,   148,   153,   159,   162,   164,   168,   172,   175,
     178,   180,   182,   184,   186,   188,   190,   192,   194,   196,
     198,   200,   202,   204,   206,   210,   214,   218,   220,   224,
     230,   236,   238,   242,   246,   249,   252,   254,   256,   260,
     264,   268,   272,   276,   280,   284,   286,   289,   291,   295,
     299,   303,   305,   308,   311,   314,   317,   319,   322,   325,
     328,   331,   334,   337,   340,   343,   346,   349,   351,   354,
     356,   360,   364,   368,   371,   378,   385,   387,   389,   391,
     395,   397,   399,   401,   403,   405,   407,   409,   411,   413,
     415,   417,   419,   421,   425,   429,   433,   437,   441,   445,
     449,   455,   461,   467,   473,   479,   485,   491,   495,   497,
     499,   503,   507,   511,   515,   519,   521,   523,   525,   529,
     533,   535,   539,   543,   547,   549,   550,   554,   558,   563,
     567,   571,   573,   575,   577,   579,   581,   583,   585,   587,
     589,   591,   593,   595,   597,   601,   605,   607,   611,   615,
     619,   623
};

/* YYRHS -- A `-1'-separated list of the rules' RHS.  */
static const yytype_int16 yyrhs[] =
{
     126,     0,    -1,    -1,   126,   127,    -1,   126,   123,    93,
      83,    -1,   126,   123,    93,    79,    -1,   126,    59,    -1,
     124,    83,   129,    -1,   119,    83,   129,    -1,   120,   129,
      -1,   124,    84,   128,    72,   129,    -1,   118,    83,   129,
      -1,    83,    45,   128,    -1,    85,    45,   128,    -1,    83,
      -1,    85,    -1,    -1,   130,     4,    -1,   131,    -1,   130,
      10,   131,    -1,   130,    11,   131,    -1,   130,     9,   131,
      -1,   130,     7,   131,    -1,   130,     6,   131,    -1,    51,
      69,   131,    45,   131,    45,   131,    70,    -1,   130,    77,
      -1,    78,   130,    -1,    76,    -1,   141,    -1,   132,    -1,
     132,    44,   133,    -1,   133,    -1,   134,    -1,   134,   136,
      -1,   134,    45,   135,    -1,   135,    -1,   131,   140,   131,
      -1,   131,   140,   131,    12,   131,    -1,   131,   140,   131,
      12,    -1,   131,   140,    12,   131,    -1,    73,    74,   140,
     131,    -1,    73,   131,    74,   140,   131,    -1,   131,   140,
      73,    74,    -1,   131,   140,    73,   131,    74,    -1,   139,
     137,    -1,   138,    -1,   137,    45,   138,    -1,   131,    13,
     131,    -1,   131,    13,    -1,    13,   131,    -1,    13,    -1,
      34,    -1,    33,    -1,    32,    -1,    31,    -1,    30,    -1,
      28,    -1,    24,    -1,    23,    -1,    22,    -1,    21,    -1,
      29,    -1,    27,    -1,   142,    -1,   141,    16,   142,    -1,
     141,    15,   142,    -1,   141,    14,   142,    -1,   145,    -1,
     145,    19,   143,    -1,   145,    20,   145,    13,   145,    -1,
     145,    18,   145,    13,   145,    -1,   144,    -1,   143,    45,
     144,    -1,   145,    13,   145,    -1,   145,    13,    -1,    13,
     145,    -1,    13,    -1,   146,    -1,   145,    40,   146,    -1,
     145,     8,   146,    -1,   145,    39,   146,    -1,   145,    38,
     146,    -1,   145,    37,   146,    -1,   145,    36,   146,    -1,
     145,    35,   146,    -1,   147,    -1,   146,   146,    -1,   148,
      -1,   147,    43,   148,    -1,   147,    42,   148,    -1,   147,
      41,   148,    -1,   149,    -1,    49,   149,    -1,    48,   149,
      -1,    47,   149,    -1,    46,   149,    -1,   150,    -1,   150,
      57,    -1,   150,    56,    -1,   150,    55,    -1,   150,    54,
      -1,   150,    53,    -1,   150,    52,    -1,   150,    68,    -1,
     150,    67,    -1,   150,    66,    -1,   150,    65,    -1,   151,
      -1,    50,   151,    -1,   152,    -1,    69,   130,    70,    -1,
     151,    75,   152,    -1,    71,   130,    72,    -1,   151,     3,
      -1,    69,   130,    70,    99,    83,    72,    -1,    69,   130,
      70,    99,    85,    72,    -1,    85,    -1,    79,    -1,    81,
      -1,   122,    83,    72,    -1,    86,    -1,    80,    -1,   153,
      -1,   154,    -1,   156,    -1,   158,    -1,   159,    -1,    87,
      -1,    88,    -1,    89,    -1,    90,    -1,    91,    -1,    92,
      -1,   117,   130,    72,    -1,   116,   130,    72,    -1,   114,
     130,    72,    -1,   112,   130,    72,    -1,   115,   130,    72,
      -1,   113,   130,    72,    -1,   111,   130,    72,    -1,   117,
     130,    45,    83,    72,    -1,   116,   130,    45,    83,    72,
      -1,   114,   130,    45,    83,    72,    -1,   112,   130,    45,
      83,    72,    -1,   115,   130,    45,    83,    72,    -1,   113,
     130,    45,    83,    72,    -1,   111,   130,    45,    83,    72,
      -1,   108,   130,    72,    -1,   161,    -1,     5,    -1,    98,
     130,    72,    -1,    97,   130,    72,    -1,    96,   157,    72,
      -1,    95,   130,    72,    -1,    94,    83,    72,    -1,   160,
      -1,   162,    -1,    83,    -1,   109,   155,    72,    -1,   110,
     155,    72,    -1,    83,    -1,    83,    45,   155,    -1,    84,
     157,    72,    -1,   130,    45,   157,    -1,   130,    -1,    -1,
     121,    83,    72,    -1,   106,   128,    72,    -1,   106,   128,
      72,    68,    -1,   107,    83,    72,    -1,   107,    85,    72,
      -1,    64,    -1,    63,    -1,    62,    -1,    61,    -1,    58,
      -1,    60,    -1,   163,    -1,   164,    -1,   165,    -1,   167,
      -1,   168,    -1,   169,    -1,   170,    -1,   101,   166,    72,
      -1,   100,   166,    72,    -1,   163,    -1,   163,    45,   166,
      -1,   104,   130,    72,    -1,   102,   130,    72,    -1,   105,
     130,    72,    -1,   103,   130,    72,    -1
};

/* YYRLINE[YYN] -- source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   109,   109,   110,   127,   131,   136,   142,   147,   154,
     158,   165,   172,   173,   174,   175,   176,   178,   188,   189,
     190,   191,   192,   193,   194,   197,   199,   201,   205,   206,
     208,   215,   219,   221,   225,   232,   234,   237,   240,   245,
     248,   250,   252,   254,   258,   262,   265,   271,   272,   273,
     274,   278,   279,   280,   281,   284,   285,   286,   287,   288,
     289,   290,   291,   294,   295,   296,   297,   299,   300,   301,
     302,   304,   309,   316,   317,   318,   319,   321,   322,   323,
     324,   325,   326,   327,   328,   330,   331,   333,   334,   335,
     336,   338,   339,   340,   341,   342,   344,   345,   346,   347,
     348,   349,   350,   351,   355,   359,   363,   370,   371,   373,
     374,   375,   376,   377,   378,   383,   390,   391,   392,   393,
     394,   399,   400,   401,   402,   404,   405,   406,   407,   408,
     409,   410,   411,   412,   413,   414,   415,   416,   417,   418,
     420,   431,   442,   453,   464,   475,   486,   497,   498,   499,
     500,   501,   502,   503,   504,   505,   506,   513,   524,   530,
     536,   538,   546,   563,   565,   566,   568,   587,   598,   610,
     613,   618,   636,   640,   644,   666,   670,   691,   692,   693,
     696,   697,   698,   699,   701,   719,   735,   738,   743,   749,
     759,   767
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || YYTOKEN_TABLE
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "WEIGHT", "END_OF_WEIGHTED_EXPRESSION",
  "CHARACTER_RANGE", "MERGE_LEFT_ARROW", "MERGE_RIGHT_ARROW",
  "INTERSECTION", "LENIENT_COMPOSITION", "COMPOSITION", "CROSS_PRODUCT",
  "MARKUP_MARKER", "CENTER_MARKER", "AFTER", "BEFORE", "SHUFFLE",
  "LEFT_RESTRICTION", "LEFT_RIGHT_ARROW", "RIGHT_ARROW", "LEFT_ARROW",
  "LTR_SHORTEST_MATCH", "LTR_LONGEST_MATCH", "RTL_SHORTEST_MATCH",
  "RTL_LONGEST_MATCH", "OPTIONAL_REPLACE_LEFT_RIGHT", "REPLACE_LEFT_RIGHT",
  "OPTIONAL_REPLACE_LEFT", "OPTIONAL_REPLACE_RIGHT", "REPLACE_LEFT",
  "REPLACE_RIGHT", "REPLACE_CONTEXT_LL", "REPLACE_CONTEXT_UL",
  "REPLACE_CONTEXT_LU", "REPLACE_CONTEXT_UU", "LOWER_PRIORITY_UNION",
  "UPPER_PRIORITY_UNION", "LOWER_MINUS", "UPPER_MINUS", "MINUS", "UNION",
  "LEFT_QUOTIENT", "IGNORE_INTERNALLY", "IGNORING", "COMMACOMMA", "COMMA",
  "CONTAINMENT_OPT", "CONTAINMENT_ONCE", "CONTAINMENT", "COMPLEMENT",
  "TERM_COMPLEMENT", "SUBSTITUTE_LEFT", "LOWER_PROJECT", "UPPER_PROJECT",
  "INVERT", "REVERSE", "PLUS", "STAR", "READ_LEXC", "READ_VEC", "READ_RE",
  "READ_PROLOG", "READ_SPACED", "READ_TEXT", "READ_BIN", "CATENATE_N_TO_K",
  "CATENATE_N_MINUS", "CATENATE_N_PLUS", "CATENATE_N", "LEFT_BRACKET",
  "RIGHT_BRACKET", "LEFT_PARENTHESIS", "RIGHT_PARENTHESIS",
  "LEFT_BRACKET_DOTTED", "RIGHT_BRACKET_DOTTED", "PAIR_SEPARATOR",
  "PAIR_SEPARATOR_SOLE", "PAIR_SEPARATOR_WO_RIGHT",
  "PAIR_SEPARATOR_WO_LEFT", "EPSILON_TOKEN", "ANY_TOKEN",
  "BOUNDARY_MARKER", "LEXER_ERROR", "SYMBOL", "SYMBOL_WITH_LEFT_PAREN",
  "QUOTED_LITERAL", "CURLY_LITERAL", "ALPHA", "LOWERALPHA", "UPPERALPHA",
  "NUM", "PUNCT", "WHITESPACE", "VARIABLE_NAME", "COUNTER_LEFT",
  "SIGMA_LEFT", "INTERPOLATE_LEFT", "EXC_LEFT", "LST_LEFT", "TAG_LEFT",
  "AND_LEFT", "OR_LEFT", "NRC_LEFT", "NLC_LEFT", "RC_LEFT", "LC_LEFT",
  "LIKE_LEFT", "ENDTAG_LEFT", "DEFINE_LEFT", "EXPLODE_LEFT",
  "IMPLODE_LEFT", "ANY_CASE_LEFT", "TOUPPER_LEFT", "OPT_TOUPPER_LEFT",
  "TOLOWER_LEFT", "OPT_TOLOWER_LEFT", "OPTCAP_LEFT", "CAP_LEFT",
  "DEFINED_LIST", "DEFINS", "REGEX", "INS_LEFT", "LIT_LEFT",
  "SET_VARIABLE", "DEFINE", "$accept", "PMATCH", "DEFINITION", "ARGLIST",
  "EXPRESSION1", "EXPRESSION2", "EXPRESSION3", "PARALLEL_RULES", "RULE",
  "MAPPINGPAIR_VECTOR", "MAPPINGPAIR", "CONTEXTS_WITH_MARK",
  "CONTEXTS_VECTOR", "CONTEXT", "CONTEXT_MARK", "REPLACE_ARROW",
  "EXPRESSION4", "EXPRESSION5", "RESTR_CONTEXTS", "RESTR_CONTEXT",
  "EXPRESSION6", "EXPRESSION7", "EXPRESSION8", "EXPRESSION9",
  "EXPRESSION10", "EXPRESSION11", "EXPRESSION12", "EXPRESSION13",
  "EXPLODE", "IMPLODE", "CONCATENATED_STRING_LIST", "FUNCALL",
  "FUNCALL_ARGLIST", "INSERTION", "LIKE", "ENDTAG", "READ_FROM",
  "CONTEXT_CONDITION", "PMATCH_CONTEXT", "PMATCH_OR_CONTEXT",
  "PMATCH_AND_CONTEXT", "PMATCH_CONTEXTS", "PMATCH_RIGHT_CONTEXT",
  "PMATCH_NEGATIVE_RIGHT_CONTEXT", "PMATCH_LEFT_CONTEXT",
  "PMATCH_NEGATIVE_LEFT_CONTEXT", 0
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
     375,   376,   377,   378,   379
};
# endif

/* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,   125,   126,   126,   126,   126,   126,   127,   127,   127,
     127,   127,   128,   128,   128,   128,   128,   129,   130,   130,
     130,   130,   130,   130,   130,   130,   130,   130,   131,   131,
     132,   132,   133,   133,   134,   134,   135,   135,   135,   135,
     135,   135,   135,   135,   136,   137,   137,   138,   138,   138,
     138,   139,   139,   139,   139,   140,   140,   140,   140,   140,
     140,   140,   140,   141,   141,   141,   141,   142,   142,   142,
     142,   143,   143,   144,   144,   144,   144,   145,   145,   145,
     145,   145,   145,   145,   145,   146,   146,   147,   147,   147,
     147,   148,   148,   148,   148,   148,   149,   149,   149,   149,
     149,   149,   149,   149,   149,   149,   149,   150,   150,   151,
     151,   151,   151,   151,   151,   151,   152,   152,   152,   152,
     152,   152,   152,   152,   152,   152,   152,   152,   152,   152,
     152,   152,   152,   152,   152,   152,   152,   152,   152,   152,
     152,   152,   152,   152,   152,   152,   152,   152,   152,   152,
     152,   152,   152,   152,   152,   152,   152,   152,   153,   154,
     155,   155,   156,   157,   157,   157,   158,   159,   159,   160,
     160,   161,   161,   161,   161,   161,   161,   162,   162,   162,
     163,   163,   163,   163,   164,   165,   166,   166,   167,   168,
     169,   170
};

/* YYR2[YYN] -- Number of symbols composing right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     0,     2,     4,     4,     2,     3,     3,     2,
       5,     3,     3,     3,     1,     1,     0,     2,     1,     3,
       3,     3,     3,     3,     8,     2,     2,     1,     1,     1,
       3,     1,     1,     2,     3,     1,     3,     5,     4,     4,
       4,     5,     4,     5,     2,     1,     3,     3,     2,     2,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     3,     3,     3,     1,     3,     5,
       5,     1,     3,     3,     2,     2,     1,     1,     3,     3,
       3,     3,     3,     3,     3,     1,     2,     1,     3,     3,
       3,     1,     2,     2,     2,     2,     1,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     1,     2,     1,
       3,     3,     3,     2,     6,     6,     1,     1,     1,     3,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     3,     3,     3,     3,     3,     3,     3,
       5,     5,     5,     5,     5,     5,     5,     3,     1,     1,
       3,     3,     3,     3,     3,     1,     1,     1,     3,     3,
       1,     3,     3,     3,     1,     0,     3,     3,     4,     3,
       3,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     3,     3,     1,     3,     3,     3,
       3,     3
};

/* YYDEFACT[STATE-NAME] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE doesn't specify something else to do.  Zero
   means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       2,     0,     1,     6,     0,     0,     0,     0,     0,     3,
       0,     0,   149,     0,     0,     0,     0,     0,     0,   175,
     176,   174,   173,   172,   171,     0,     0,     0,    27,     0,
     117,   121,   118,   157,   165,   116,   120,   127,   128,   129,
     130,   131,   132,     0,     0,   165,     0,     0,     0,     0,
       0,     0,     0,     0,    16,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     9,     0,
      18,    29,    31,    32,    35,    28,    63,    67,    77,    85,
      87,    91,    96,   107,   109,   122,   123,   124,   125,   126,
     155,   148,   156,   177,   178,   179,   180,   181,   182,   183,
       0,     0,    16,    11,     8,    95,    94,    93,    92,   108,
       0,     0,     0,     0,     0,    26,   164,     0,     0,     0,
       0,     0,     0,   186,     0,     0,     0,     0,     0,     0,
      14,    15,     0,     0,     0,     0,   160,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,    17,     0,
       0,     0,     0,     0,    25,    60,    59,    58,    57,    62,
      56,    61,    55,     0,     0,    54,    53,    52,    51,     0,
      33,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,    86,     0,     0,     0,   102,
     101,   100,    99,    98,    97,   106,   105,   104,   103,   113,
       0,     5,     4,     7,     0,     0,   110,   112,     0,     0,
     165,   162,   154,   153,   152,   151,   150,     0,   185,   184,
     189,   191,   188,   190,    16,    16,   167,   169,   170,   147,
       0,   158,   159,     0,   139,     0,   136,     0,   138,     0,
     135,     0,   137,     0,   134,     0,   133,   166,   119,    23,
      22,    21,    19,    20,     0,     0,    36,     0,    30,    34,
      50,     0,    44,    45,    66,    65,    64,    79,     0,    76,
      68,    71,     0,     0,    84,    83,    82,    81,    80,    78,
      90,    89,    88,   111,     0,     0,     0,    40,     0,   163,
     187,    12,    13,   168,   161,     0,     0,     0,     0,     0,
       0,     0,    39,    42,     0,    38,    49,    48,     0,     0,
      75,     0,    74,     0,    10,     0,     0,     0,    41,   146,
     143,   145,   142,   144,   141,   140,    43,    37,    47,    46,
      70,    72,    73,    69,     0,   114,   115,     0,    24
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,     1,     9,   132,    68,    69,    70,    71,    72,    73,
      74,   170,   262,   263,   171,   163,    75,    76,   270,   271,
      77,    78,    79,    80,    81,    82,    83,    84,    85,    86,
     137,    87,   117,    88,    89,    90,    91,    92,    93,    94,
      95,   124,    96,    97,    98,    99
};

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
#define YYPACT_NINF -157
static const yytype_int16 yypact[] =
{
    -157,    89,  -157,  -157,   -45,   -35,   237,   -64,   -60,  -157,
     237,   237,  -157,   952,   952,   952,   952,  1017,   -33,  -157,
    -157,  -157,  -157,  -157,  -157,   237,   237,   314,  -157,   237,
    -157,  -157,  -157,  -157,   237,  -157,  -157,  -157,  -157,  -157,
    -157,  -157,  -157,   -24,   237,   237,   237,   237,   -47,   -47,
     237,   237,   237,   237,    -1,     2,   237,   -20,   -20,   237,
     237,   237,   237,   237,   237,   237,   -14,   -10,  -157,    43,
    1288,     7,  -157,   -15,  -157,   101,  -157,   538,   884,    62,
    -157,  -157,   414,    11,  -157,  -157,  -157,  -157,  -157,  -157,
    -157,  -157,  -157,  -157,  -157,  -157,  -157,  -157,  -157,  -157,
     -44,   237,    -1,  -157,  -157,  -157,  -157,  -157,  -157,    11,
     694,    61,   158,  1288,   216,   253,   189,   -12,     9,   164,
      19,  1018,  1147,    29,    25,    26,  1219,  1225,  1231,  1242,
      32,    56,    46,    47,    49,  1248,    88,    67,    68,    55,
      69,   152,   176,  1199,  1205,  1211,    71,    73,  -157,   694,
     694,   694,   694,   694,  -157,  -157,  -157,  -157,  -157,  -157,
    -157,  -157,  -157,   427,   694,  -157,  -157,  -157,  -157,   694,
    -157,   540,   884,   884,   884,   884,   884,   807,   884,   884,
     884,   884,   884,   884,   884,   884,   884,   884,   884,  -157,
    -157,  -157,  -157,  -157,  -157,  -157,  -157,  -157,  -157,  -157,
    1082,  -157,  -157,  -157,    75,   801,    53,  -157,   694,  1288,
     237,  -157,  -157,  -157,  -157,  -157,  -157,   -47,  -157,  -157,
    -157,  -157,  -157,  -157,    -1,    -1,    86,  -157,  -157,  -157,
     -20,  -157,  -157,    77,  -157,    83,  -157,    97,  -157,   105,
    -157,   106,  -157,   107,  -157,   109,  -157,  -157,  -157,  1288,
    1288,  1288,  1288,  1288,   694,   617,  1277,  1288,  -157,  -157,
     694,  1251,   127,  -157,  -157,  -157,  -157,   884,   425,   884,
     139,  -157,   556,   805,   884,   884,   884,   884,   884,   884,
    -157,  -157,  -157,  -157,   237,   694,     5,  1288,   694,  -157,
    -157,  -157,  -157,  -157,  -157,   138,   142,   143,   145,   146,
     147,   148,  1288,  1288,   419,   694,  1288,   694,   540,   884,
     544,   807,   884,   884,  -157,  1239,   150,   151,  1288,  -157,
    -157,  -157,  -157,  -157,  -157,  -157,  1288,  1288,  1288,  -157,
     544,  -157,   544,   544,   694,  -157,  -157,   429,  -157
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -157,  -157,  -157,   -90,    -9,   -19,   -27,  -157,    85,  -157,
      42,  -157,  -157,   -83,  -157,  -110,  -157,   -23,  -157,   -85,
    -156,   -73,  -157,   -58,    80,  -157,   214,    50,  -157,  -157,
     -54,  -157,   -32,  -157,  -157,  -157,  -157,  -157,   -40,  -157,
    -157,   -38,  -157,  -157,  -157,  -157
};

/* YYTABLE[YYPACT[STATE-NUM]].  What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule which
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
#define YYTABLE_NINF -1
static const yytype_uint16 yytable[] =
{
     114,   103,   104,   208,   138,   185,   111,   112,   123,   123,
     115,   125,   204,   120,   199,   116,   165,   166,   167,   168,
     268,   272,   273,   101,   102,   119,   116,   121,   122,   100,
     169,   126,   127,   128,   129,   201,   110,   135,    10,   202,
     139,   140,   141,   142,   143,   144,   145,   148,    11,   149,
     150,   164,   151,   152,   153,    50,    51,    52,    53,   118,
     211,   149,   150,   136,   151,   152,   153,   149,   150,   146,
     151,   152,   153,   147,   217,   149,   150,   224,   151,   152,
     153,   212,   130,   205,   131,   133,   200,   134,   316,     2,
     317,   214,   203,   105,   106,   107,   108,   218,   219,   288,
     233,   225,   267,   186,   187,   188,   274,   275,   276,   277,
     278,   279,   185,   310,   235,   172,   173,   174,   226,   227,
     154,   228,   249,   250,   251,   252,   253,   234,   280,   281,
     282,   206,   154,   230,   291,   292,   256,   257,   154,   231,
     232,   236,   257,   247,   261,   248,   154,   284,     3,   264,
     265,   266,   286,   330,   293,   272,   332,   333,   149,   150,
     295,   151,   152,   153,   149,   150,   296,   151,   152,   153,
     149,   150,   308,   151,   152,   153,   294,   123,   289,   290,
     297,   287,   149,   150,   311,   151,   152,   153,   298,   299,
     300,   116,   301,   208,   185,   149,   150,   237,   151,   152,
     153,   185,   185,   185,   185,   185,   185,     4,     5,     6,
     319,   259,     7,     8,   320,   321,   288,   322,   323,   324,
     325,   239,   335,   336,   238,   329,   331,   302,   304,   154,
     207,   109,     0,   306,   210,   154,   213,   155,   156,   157,
     158,   154,    12,   159,   160,   161,   162,     0,   240,   258,
     283,     0,     0,   154,     0,     0,     0,     0,   315,   149,
     150,   318,   151,   152,   153,     0,   154,     0,     0,     0,
       0,     0,     0,     0,     0,   314,     0,     0,   327,     0,
     328,   261,     0,    13,    14,    15,    16,    17,    18,     0,
     209,     0,     0,     0,     0,    19,     0,    20,    21,    22,
      23,    24,     0,     0,     0,     0,    25,   337,    26,     0,
      27,     0,     0,    28,     0,    29,    30,    31,    32,    12,
      33,    34,    35,    36,    37,    38,    39,    40,    41,    42,
     154,    43,    44,    45,    46,    47,     0,    48,    49,    50,
      51,    52,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,    63,    64,    65,     0,     0,     0,    66,    67,
      13,    14,    15,    16,    17,     0,     0,     0,     0,     0,
       0,     0,    19,     0,    20,    21,    22,    23,    24,     0,
       0,     0,     0,    25,     0,    26,     0,    27,   113,     0,
       0,     0,     0,    30,    31,    32,     0,    33,    34,    35,
      36,    37,    38,    39,    40,    41,    42,     0,    43,    44,
      45,    46,    47,     0,    48,    49,    50,    51,    52,    53,
      54,    55,    56,    57,    58,    59,    60,    61,    62,    63,
      64,    65,    12,   175,     0,    66,    67,     0,   309,   254,
     155,   156,   157,   158,     0,     0,   159,   160,   161,   162,
     155,   156,   157,   158,     0,     0,   159,   160,   161,   162,
     179,   180,   181,   182,   183,   184,   189,   190,   191,   192,
     193,   194,     0,    13,    14,    15,    16,    17,     0,   195,
     196,   197,   198,     0,     0,    19,     0,    20,    21,    22,
      23,    24,     0,   326,     0,     0,    25,     0,    26,   338,
     255,     0,     0,     0,     0,     0,    30,    31,    32,     0,
      33,    34,    35,    36,    37,    38,    39,    40,    41,    42,
       0,    43,    44,    45,    46,    47,     0,    48,    49,    50,
      51,    52,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,    63,    64,    65,    12,   175,     0,    66,    67,
       0,     0,   175,   260,     0,     0,   176,   177,   178,     0,
       0,     0,     0,     0,   175,     0,     0,     0,     0,   312,
       0,     0,     0,   179,   180,   181,   182,   183,   184,   179,
     180,   181,   182,   183,   184,     0,    13,    14,    15,    16,
      17,   179,   180,   181,   182,   183,   184,     0,    19,     0,
      20,    21,    22,    23,    24,     0,     0,     0,     0,    25,
       0,    26,     0,    27,     0,     0,     0,     0,     0,    30,
      31,    32,    12,    33,    34,    35,    36,    37,    38,    39,
      40,    41,    42,     0,    43,    44,    45,    46,    47,     0,
      48,    49,    50,    51,    52,    53,    54,    55,    56,    57,
      58,    59,    60,    61,    62,    63,    64,    65,     0,     0,
       0,    66,    67,    13,    14,    15,    16,    17,     0,     0,
       0,     0,     0,     0,     0,    19,     0,    20,    21,    22,
      23,    24,     0,     0,     0,     0,    25,     0,    26,     0,
      27,   303,     0,     0,     0,     0,    30,    31,    32,    12,
      33,    34,    35,    36,    37,    38,    39,    40,    41,    42,
       0,    43,    44,    45,    46,    47,     0,    48,    49,    50,
      51,    52,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,    63,    64,    65,     0,     0,     0,    66,    67,
      13,    14,    15,    16,    17,     0,     0,     0,     0,     0,
       0,     0,    19,     0,    20,    21,    22,    23,    24,     0,
       0,     0,     0,    25,     0,    26,     0,    27,     0,     0,
       0,     0,     0,    30,    31,    32,     0,    33,    34,    35,
      36,    37,    38,    39,    40,    41,    42,     0,    43,    44,
      45,    46,    47,     0,    48,    49,    50,    51,    52,    53,
      54,    55,    56,    57,    58,    59,    60,    61,    62,    63,
      64,    65,    12,   175,     0,    66,    67,     0,   313,     0,
     269,     0,   155,   156,   157,   158,     0,     0,   159,   160,
     161,   162,     0,     0,     0,     0,     0,     0,     0,     0,
     179,   180,   181,   182,   183,   184,   285,     0,     0,     0,
       0,     0,     0,    13,    14,    15,    16,    17,     0,     0,
       0,     0,     0,     0,     0,    19,     0,    20,    21,    22,
      23,    24,     0,     0,     0,     0,    25,     0,    26,     0,
       0,     0,     0,     0,     0,     0,    30,    31,    32,    12,
      33,    34,    35,    36,    37,    38,    39,    40,    41,    42,
       0,    43,    44,    45,    46,    47,     0,    48,    49,    50,
      51,    52,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,    63,    64,    65,     0,     0,     0,    66,    67,
      13,    14,    15,    16,    17,     0,     0,     0,     0,     0,
       0,     0,    19,     0,    20,    21,    22,    23,    24,     0,
       0,     0,     0,    25,     0,    26,     0,    12,     0,     0,
       0,     0,     0,    30,    31,    32,     0,    33,    34,    35,
      36,    37,    38,    39,    40,    41,    42,     0,    43,    44,
      45,    46,    47,     0,    48,    49,    50,    51,    52,    53,
      54,    55,    56,    57,    58,    59,    60,    61,    62,    63,
      64,    65,    17,     0,     0,    66,    67,     0,     0,     0,
      19,     0,    20,    21,    22,    23,    24,     0,     0,     0,
       0,    25,    12,    26,   149,   150,     0,   151,   152,   153,
       0,    30,    31,    32,     0,    33,    34,    35,    36,    37,
      38,    39,    40,    41,    42,     0,    43,    44,    45,    46,
      47,     0,    48,    49,    50,    51,    52,    53,    54,    55,
      56,    57,    58,    59,    60,    61,    62,    63,    64,    65,
       0,     0,     0,    66,    67,    19,     0,    20,    21,    22,
      23,    24,     0,     0,     0,     0,    25,    12,    26,     0,
     215,     0,     0,     0,     0,   154,    30,    31,    32,     0,
      33,    34,    35,    36,    37,    38,    39,    40,    41,    42,
       0,    43,    44,    45,    46,    47,     0,    48,    49,    50,
      51,    52,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,    63,    64,    65,     0,     0,     0,    66,    67,
      19,     0,    20,    21,    22,    23,    24,     0,     0,     0,
       0,     0,     0,   149,   150,     0,   151,   152,   153,     0,
       0,    30,    31,    32,     0,    33,    34,    35,    36,    37,
      38,    39,    40,    41,    42,     0,    43,    44,    45,    46,
      47,     0,    48,    49,    50,    51,    52,    53,    54,    55,
      56,    57,    58,    59,    60,    61,    62,    63,    64,    65,
       0,     0,     0,    66,    67,   149,   150,     0,   151,   152,
     153,   149,   150,     0,   151,   152,   153,   149,   150,   216,
     151,   152,   153,     0,   154,   149,   150,     0,   151,   152,
     153,   149,   150,     0,   151,   152,   153,   149,   150,     0,
     151,   152,   153,     0,   241,     0,     0,     0,   149,   150,
     243,   151,   152,   153,   149,   150,   245,   151,   152,   153,
     155,   156,   157,   158,   307,     0,   159,   160,   161,   162,
       0,   242,   155,   156,   157,   158,   154,   244,   159,   160,
     161,   162,   154,   246,   334,     0,     0,     0,   154,   305,
       0,   220,     0,     0,     0,     0,   154,   221,   155,   156,
     157,   158,   154,   222,   159,   160,   161,   162,   154,   155,
     156,   157,   158,     0,   223,   159,   160,   161,   162,   154,
     229,     0,     0,     0,     0,   154
};

#define yypact_value_is_default(yystate) \
  ((yystate) == (-157))

#define yytable_value_is_error(yytable_value) \
  YYID (0)

static const yytype_int16 yycheck[] =
{
      27,    10,    11,   113,    58,    78,    25,    26,    48,    49,
      29,    49,   102,    45,     3,    34,    31,    32,    33,    34,
     176,   177,   178,    83,    84,    44,    45,    46,    47,    93,
      45,    50,    51,    52,    53,    79,    69,    56,    83,    83,
      59,    60,    61,    62,    63,    64,    65,     4,    83,     6,
       7,    44,     9,    10,    11,   102,   103,   104,   105,    83,
      72,     6,     7,    83,     9,    10,    11,     6,     7,    83,
       9,    10,    11,    83,    45,     6,     7,    45,     9,    10,
      11,    72,    83,   110,    85,    83,    75,    85,    83,     0,
      85,    72,   101,    13,    14,    15,    16,    72,    72,   209,
      45,    45,   175,    41,    42,    43,   179,   180,   181,   182,
     183,   184,   185,   269,    45,    14,    15,    16,    72,    72,
      77,    72,   149,   150,   151,   152,   153,    72,   186,   187,
     188,    70,    77,    45,   224,   225,   163,   164,    77,    72,
      72,    72,   169,    72,   171,    72,    77,    72,    59,   172,
     173,   174,    99,   309,    68,   311,   312,   313,     6,     7,
      83,     9,    10,    11,     6,     7,    83,     9,    10,    11,
       6,     7,    45,     9,    10,    11,   230,   217,   210,   217,
      83,   208,     6,     7,    45,     9,    10,    11,    83,    83,
      83,   210,    83,   303,   267,     6,     7,    45,     9,    10,
      11,   274,   275,   276,   277,   278,   279,   118,   119,   120,
      72,   169,   123,   124,    72,    72,   326,    72,    72,    72,
      72,    45,    72,    72,    72,   308,   311,   254,   255,    77,
      72,    17,    -1,   260,    45,    77,    72,    21,    22,    23,
      24,    77,     5,    27,    28,    29,    30,    -1,    72,   164,
     200,    -1,    -1,    77,    -1,    -1,    -1,    -1,   285,     6,
       7,   288,     9,    10,    11,    -1,    77,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,   284,    -1,    -1,   305,    -1,
     307,   308,    -1,    46,    47,    48,    49,    50,    51,    -1,
      74,    -1,    -1,    -1,    -1,    58,    -1,    60,    61,    62,
      63,    64,    -1,    -1,    -1,    -1,    69,   334,    71,    -1,
      73,    -1,    -1,    76,    -1,    78,    79,    80,    81,     5,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
      77,    94,    95,    96,    97,    98,    -1,   100,   101,   102,
     103,   104,   105,   106,   107,   108,   109,   110,   111,   112,
     113,   114,   115,   116,   117,    -1,    -1,    -1,   121,   122,
      46,    47,    48,    49,    50,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    58,    -1,    60,    61,    62,    63,    64,    -1,
      -1,    -1,    -1,    69,    -1,    71,    -1,    73,    74,    -1,
      -1,    -1,    -1,    79,    80,    81,    -1,    83,    84,    85,
      86,    87,    88,    89,    90,    91,    92,    -1,    94,    95,
      96,    97,    98,    -1,   100,   101,   102,   103,   104,   105,
     106,   107,   108,   109,   110,   111,   112,   113,   114,   115,
     116,   117,     5,     8,    -1,   121,   122,    -1,    13,    12,
      21,    22,    23,    24,    -1,    -1,    27,    28,    29,    30,
      21,    22,    23,    24,    -1,    -1,    27,    28,    29,    30,
      35,    36,    37,    38,    39,    40,    52,    53,    54,    55,
      56,    57,    -1,    46,    47,    48,    49,    50,    -1,    65,
      66,    67,    68,    -1,    -1,    58,    -1,    60,    61,    62,
      63,    64,    -1,    74,    -1,    -1,    69,    -1,    71,    70,
      73,    -1,    -1,    -1,    -1,    -1,    79,    80,    81,    -1,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
      -1,    94,    95,    96,    97,    98,    -1,   100,   101,   102,
     103,   104,   105,   106,   107,   108,   109,   110,   111,   112,
     113,   114,   115,   116,   117,     5,     8,    -1,   121,   122,
      -1,    -1,     8,    13,    -1,    -1,    18,    19,    20,    -1,
      -1,    -1,    -1,    -1,     8,    -1,    -1,    -1,    -1,    13,
      -1,    -1,    -1,    35,    36,    37,    38,    39,    40,    35,
      36,    37,    38,    39,    40,    -1,    46,    47,    48,    49,
      50,    35,    36,    37,    38,    39,    40,    -1,    58,    -1,
      60,    61,    62,    63,    64,    -1,    -1,    -1,    -1,    69,
      -1,    71,    -1,    73,    -1,    -1,    -1,    -1,    -1,    79,
      80,    81,     5,    83,    84,    85,    86,    87,    88,    89,
      90,    91,    92,    -1,    94,    95,    96,    97,    98,    -1,
     100,   101,   102,   103,   104,   105,   106,   107,   108,   109,
     110,   111,   112,   113,   114,   115,   116,   117,    -1,    -1,
      -1,   121,   122,    46,    47,    48,    49,    50,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    58,    -1,    60,    61,    62,
      63,    64,    -1,    -1,    -1,    -1,    69,    -1,    71,    -1,
      73,    74,    -1,    -1,    -1,    -1,    79,    80,    81,     5,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
      -1,    94,    95,    96,    97,    98,    -1,   100,   101,   102,
     103,   104,   105,   106,   107,   108,   109,   110,   111,   112,
     113,   114,   115,   116,   117,    -1,    -1,    -1,   121,   122,
      46,    47,    48,    49,    50,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    58,    -1,    60,    61,    62,    63,    64,    -1,
      -1,    -1,    -1,    69,    -1,    71,    -1,    73,    -1,    -1,
      -1,    -1,    -1,    79,    80,    81,    -1,    83,    84,    85,
      86,    87,    88,    89,    90,    91,    92,    -1,    94,    95,
      96,    97,    98,    -1,   100,   101,   102,   103,   104,   105,
     106,   107,   108,   109,   110,   111,   112,   113,   114,   115,
     116,   117,     5,     8,    -1,   121,   122,    -1,    13,    -1,
      13,    -1,    21,    22,    23,    24,    -1,    -1,    27,    28,
      29,    30,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      35,    36,    37,    38,    39,    40,    45,    -1,    -1,    -1,
      -1,    -1,    -1,    46,    47,    48,    49,    50,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    58,    -1,    60,    61,    62,
      63,    64,    -1,    -1,    -1,    -1,    69,    -1,    71,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    79,    80,    81,     5,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
      -1,    94,    95,    96,    97,    98,    -1,   100,   101,   102,
     103,   104,   105,   106,   107,   108,   109,   110,   111,   112,
     113,   114,   115,   116,   117,    -1,    -1,    -1,   121,   122,
      46,    47,    48,    49,    50,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    58,    -1,    60,    61,    62,    63,    64,    -1,
      -1,    -1,    -1,    69,    -1,    71,    -1,     5,    -1,    -1,
      -1,    -1,    -1,    79,    80,    81,    -1,    83,    84,    85,
      86,    87,    88,    89,    90,    91,    92,    -1,    94,    95,
      96,    97,    98,    -1,   100,   101,   102,   103,   104,   105,
     106,   107,   108,   109,   110,   111,   112,   113,   114,   115,
     116,   117,    50,    -1,    -1,   121,   122,    -1,    -1,    -1,
      58,    -1,    60,    61,    62,    63,    64,    -1,    -1,    -1,
      -1,    69,     5,    71,     6,     7,    -1,     9,    10,    11,
      -1,    79,    80,    81,    -1,    83,    84,    85,    86,    87,
      88,    89,    90,    91,    92,    -1,    94,    95,    96,    97,
      98,    -1,   100,   101,   102,   103,   104,   105,   106,   107,
     108,   109,   110,   111,   112,   113,   114,   115,   116,   117,
      -1,    -1,    -1,   121,   122,    58,    -1,    60,    61,    62,
      63,    64,    -1,    -1,    -1,    -1,    69,     5,    71,    -1,
      72,    -1,    -1,    -1,    -1,    77,    79,    80,    81,    -1,
      83,    84,    85,    86,    87,    88,    89,    90,    91,    92,
      -1,    94,    95,    96,    97,    98,    -1,   100,   101,   102,
     103,   104,   105,   106,   107,   108,   109,   110,   111,   112,
     113,   114,   115,   116,   117,    -1,    -1,    -1,   121,   122,
      58,    -1,    60,    61,    62,    63,    64,    -1,    -1,    -1,
      -1,    -1,    -1,     6,     7,    -1,     9,    10,    11,    -1,
      -1,    79,    80,    81,    -1,    83,    84,    85,    86,    87,
      88,    89,    90,    91,    92,    -1,    94,    95,    96,    97,
      98,    -1,   100,   101,   102,   103,   104,   105,   106,   107,
     108,   109,   110,   111,   112,   113,   114,   115,   116,   117,
      -1,    -1,    -1,   121,   122,     6,     7,    -1,     9,    10,
      11,     6,     7,    -1,     9,    10,    11,     6,     7,    72,
       9,    10,    11,    -1,    77,     6,     7,    -1,     9,    10,
      11,     6,     7,    -1,     9,    10,    11,     6,     7,    -1,
       9,    10,    11,    -1,    45,    -1,    -1,    -1,     6,     7,
      45,     9,    10,    11,     6,     7,    45,     9,    10,    11,
      21,    22,    23,    24,    13,    -1,    27,    28,    29,    30,
      -1,    72,    21,    22,    23,    24,    77,    72,    27,    28,
      29,    30,    77,    72,    45,    -1,    -1,    -1,    77,    12,
      -1,    72,    -1,    -1,    -1,    -1,    77,    72,    21,    22,
      23,    24,    77,    72,    27,    28,    29,    30,    77,    21,
      22,    23,    24,    -1,    72,    27,    28,    29,    30,    77,
      72,    -1,    -1,    -1,    -1,    77
};

/* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
   symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,   126,     0,    59,   118,   119,   120,   123,   124,   127,
      83,    83,     5,    46,    47,    48,    49,    50,    51,    58,
      60,    61,    62,    63,    64,    69,    71,    73,    76,    78,
      79,    80,    81,    83,    84,    85,    86,    87,    88,    89,
      90,    91,    92,    94,    95,    96,    97,    98,   100,   101,
     102,   103,   104,   105,   106,   107,   108,   109,   110,   111,
     112,   113,   114,   115,   116,   117,   121,   122,   129,   130,
     131,   132,   133,   134,   135,   141,   142,   145,   146,   147,
     148,   149,   150,   151,   152,   153,   154,   156,   158,   159,
     160,   161,   162,   163,   164,   165,   167,   168,   169,   170,
      93,    83,    84,   129,   129,   149,   149,   149,   149,   151,
      69,   130,   130,    74,   131,   130,   130,   157,    83,   130,
     157,   130,   130,   163,   166,   166,   130,   130,   130,   130,
      83,    85,   128,    83,    85,   130,    83,   155,   155,   130,
     130,   130,   130,   130,   130,   130,    83,    83,     4,     6,
       7,     9,    10,    11,    77,    21,    22,    23,    24,    27,
      28,    29,    30,   140,    44,    31,    32,    33,    34,    45,
     136,   139,    14,    15,    16,     8,    18,    19,    20,    35,
      36,    37,    38,    39,    40,   146,    41,    42,    43,    52,
      53,    54,    55,    56,    57,    65,    66,    67,    68,     3,
      75,    79,    83,   129,   128,   131,    70,    72,   140,    74,
      45,    72,    72,    72,    72,    72,    72,    45,    72,    72,
      72,    72,    72,    72,    45,    45,    72,    72,    72,    72,
      45,    72,    72,    45,    72,    45,    72,    45,    72,    45,
      72,    45,    72,    45,    72,    45,    72,    72,    72,   131,
     131,   131,   131,   131,    12,    73,   131,   131,   133,   135,
      13,   131,   137,   138,   142,   142,   142,   146,   145,    13,
     143,   144,   145,   145,   146,   146,   146,   146,   146,   146,
     148,   148,   148,   152,    72,    45,    99,   131,   140,   157,
     166,   128,   128,    68,   155,    83,    83,    83,    83,    83,
      83,    83,   131,    74,   131,    12,   131,    13,    45,    13,
     145,    45,    13,    13,   129,   131,    83,    85,   131,    72,
      72,    72,    72,    72,    72,    72,    74,   131,   131,   138,
     145,   144,   145,   145,    45,    72,    72,   131,    70
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


/* This macro is provided for backward compatibility. */

#ifndef YY_LOCATION_PRINT
# define YY_LOCATION_PRINT(File, Loc) ((void) 0)
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
		  Type, Value); \
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
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_value_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (!yyvaluep)
    return;
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
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (yytype < YYNTOKENS)
    YYFPRINTF (yyoutput, "token %s (", yytname[yytype]);
  else
    YYFPRINTF (yyoutput, "nterm %s (", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
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
yy_reduce_print (YYSTYPE *yyvsp, int yyrule)
#else
static void
yy_reduce_print (yyvsp, yyrule)
    YYSTYPE *yyvsp;
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
		       		       );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)		\
do {					\
  if (yydebug)				\
    yy_reduce_print (yyvsp, Rule); \
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
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
#else
static void
yydestruct (yymsg, yytype, yyvaluep)
    const char *yymsg;
    int yytype;
    YYSTYPE *yyvaluep;
#endif
{
  YYUSE (yyvaluep);

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

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yytoken = 0;
  yyss = yyssa;
  yyvs = yyvsa;
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

	/* Each stack pointer address is followed by the size of the
	   data in use in that stack, in bytes.  This used to be a
	   conditional around just the two extra args, but that might
	   be undefined if yyoverflow is a macro.  */
	yyoverflow (YY_("memory exhausted"),
		    &yyss1, yysize * sizeof (*yyssp),
		    &yyvs1, yysize * sizeof (*yyvsp),
		    &yystacksize);

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
#  undef YYSTACK_RELOCATE
	if (yyss1 != yyssa)
	  YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

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


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 3:

/* Line 1806 of yacc.c  */
#line 110 "pmatch_parse.yy"
    {
    if (verbose) {
        std::cerr << std::setiosflags(std::ios::fixed) << std::setprecision(2);
        double duration = (clock() - timer) /
            (double) CLOCKS_PER_SEC;
        timer = clock();
        std::cerr << "defined " << (yyvsp[(2) - (2)].pmatchDefinition)->first << " in " << duration << " seconds\n";
    }
    if (definitions.count((yyvsp[(2) - (2)].pmatchDefinition)->first) != 0) {
        std::stringstream warning;
        warning << "definition of " << (yyvsp[(2) - (2)].pmatchDefinition)->first << " on line " << pmatchlineno
                << " shadows earlier definition\n";
        warn(warning.str());
        delete definitions[(yyvsp[(2) - (2)].pmatchDefinition)->first];
    }
    definitions.insert(*(yyvsp[(2) - (2)].pmatchDefinition));
 }
    break;

  case 4:

/* Line 1806 of yacc.c  */
#line 127 "pmatch_parse.yy"
    {
    hfst::pmatch::variables[(yyvsp[(3) - (4)].label)] = (yyvsp[(4) - (4)].label);
    free((yyvsp[(3) - (4)].label)); free((yyvsp[(4) - (4)].label));
 }
    break;

  case 5:

/* Line 1806 of yacc.c  */
#line 131 "pmatch_parse.yy"
    {
     // the symbol can be 0, and that pretty much has to be reserved for
     // epsilon, so we detect that possibility here
     hfst::pmatch::variables[(yyvsp[(3) - (4)].label)] = "0";
     free((yyvsp[(3) - (4)].label));
 }
    break;

  case 6:

/* Line 1806 of yacc.c  */
#line 136 "pmatch_parse.yy"
    {
     std::string filepath = hfst::pmatch::path_from_filename((yyvsp[(2) - (2)].label));
     free((yyvsp[(2) - (2)].label));
     hfst::pmatch::read_vec(filepath);
   }
    break;

  case 7:

/* Line 1806 of yacc.c  */
#line 142 "pmatch_parse.yy"
    {
    (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject*>((yyvsp[(2) - (3)].label), (yyvsp[(3) - (3)].pmatchObject));
    (yyvsp[(3) - (3)].pmatchObject)->name = (yyvsp[(2) - (3)].label);
    free((yyvsp[(2) - (3)].label));
 }
    break;

  case 8:

/* Line 1806 of yacc.c  */
#line 147 "pmatch_parse.yy"
    {
     (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject*>(
         (yyvsp[(2) - (3)].label), new PmatchString(get_Ins_transition((yyvsp[(2) - (3)].label))));
     def_insed_expressions[(yyvsp[(2) - (3)].label)] = (yyvsp[(3) - (3)].pmatchObject);
     (yyvsp[(3) - (3)].pmatchObject)->name = (yyvsp[(2) - (3)].label);
     free((yyvsp[(2) - (3)].label));
 }
    break;

  case 9:

/* Line 1806 of yacc.c  */
#line 154 "pmatch_parse.yy"
    {
     (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject*>("TOP", (yyvsp[(2) - (2)].pmatchObject));
     (yyvsp[(2) - (2)].pmatchObject)->name = "TOP";
 }
    break;

  case 10:

/* Line 1806 of yacc.c  */
#line 158 "pmatch_parse.yy"
    {
     PmatchFunction * fun = new PmatchFunction(*(yyvsp[(3) - (5)].string_vector), (yyvsp[(5) - (5)].pmatchObject));
     fun->name = (yyvsp[(2) - (5)].label);
     (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject*>(std::string((yyvsp[(2) - (5)].label)), fun);
     function_names.insert((yyvsp[(2) - (5)].label));
     free((yyvsp[(2) - (5)].label));
 }
    break;

  case 11:

/* Line 1806 of yacc.c  */
#line 165 "pmatch_parse.yy"
    {
     (yyval.pmatchDefinition) = new std::pair<std::string, PmatchObject *>(
         (yyvsp[(2) - (3)].label), new PmatchUnaryOperation(MakeSigma, (yyvsp[(3) - (3)].pmatchObject)));
     (yyvsp[(3) - (3)].pmatchObject)->name = (yyvsp[(2) - (3)].label);
 }
    break;

  case 12:

/* Line 1806 of yacc.c  */
#line 172 "pmatch_parse.yy"
    { (yyval.string_vector) = (yyvsp[(3) - (3)].string_vector); (yyval.string_vector)->push_back(std::string((yyvsp[(1) - (3)].label))); free((yyvsp[(1) - (3)].label)); }
    break;

  case 13:

/* Line 1806 of yacc.c  */
#line 173 "pmatch_parse.yy"
    { (yyval.string_vector) = (yyvsp[(3) - (3)].string_vector); (yyval.string_vector)->push_back(std::string((yyvsp[(1) - (3)].label))); free((yyvsp[(1) - (3)].label)); }
    break;

  case 14:

/* Line 1806 of yacc.c  */
#line 174 "pmatch_parse.yy"
    { (yyval.string_vector) = new std::vector<std::string>(1, std::string((yyvsp[(1) - (1)].label))); free((yyvsp[(1) - (1)].label)); }
    break;

  case 15:

/* Line 1806 of yacc.c  */
#line 175 "pmatch_parse.yy"
    { (yyval.string_vector) = new std::vector<std::string>(1, std::string((yyvsp[(1) - (1)].label))); free((yyvsp[(1) - (1)].label)); }
    break;

  case 16:

/* Line 1806 of yacc.c  */
#line 176 "pmatch_parse.yy"
    { (yyval.string_vector) = new std::vector<std::string>(); }
    break;

  case 17:

/* Line 1806 of yacc.c  */
#line 178 "pmatch_parse.yy"
    {
     (yyvsp[(1) - (2)].pmatchObject)->weight += (yyvsp[(2) - (2)].weight);
     if (need_delimiters) {
         (yyval.pmatchObject) = new PmatchUnaryOperation(AddDelimiters, (yyvsp[(1) - (2)].pmatchObject));
     } else {
         (yyval.pmatchObject) = (yyvsp[(1) - (2)].pmatchObject);
     }
     need_delimiters = false;
}
    break;

  case 18:

/* Line 1806 of yacc.c  */
#line 188 "pmatch_parse.yy"
    {}
    break;

  case 19:

/* Line 1806 of yacc.c  */
#line 189 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Compose, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 20:

/* Line 1806 of yacc.c  */
#line 190 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(CrossProduct, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 21:

/* Line 1806 of yacc.c  */
#line 191 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(LenientCompose, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 22:

/* Line 1806 of yacc.c  */
#line 192 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Merge, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject));}
    break;

  case 23:

/* Line 1806 of yacc.c  */
#line 193 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Merge, (yyvsp[(3) - (3)].pmatchObject), (yyvsp[(1) - (3)].pmatchObject)); }
    break;

  case 24:

/* Line 1806 of yacc.c  */
#line 194 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchTernaryOperation(Substitute, (yyvsp[(3) - (8)].pmatchObject), (yyvsp[(5) - (8)].pmatchObject), (yyvsp[(7) - (8)].pmatchObject));
}
    break;

  case 25:

/* Line 1806 of yacc.c  */
#line 197 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchBinaryOperation(CrossProduct, (yyvsp[(1) - (2)].pmatchObject), new PmatchQuestionMark); }
    break;

  case 26:

/* Line 1806 of yacc.c  */
#line 199 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchBinaryOperation(CrossProduct, new PmatchQuestionMark, (yyvsp[(2) - (2)].pmatchObject)); }
    break;

  case 27:

/* Line 1806 of yacc.c  */
#line 201 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchQuestionMark;
}
    break;

  case 28:

/* Line 1806 of yacc.c  */
#line 205 "pmatch_parse.yy"
    { }
    break;

  case 29:

/* Line 1806 of yacc.c  */
#line 206 "pmatch_parse.yy"
    { }
    break;

  case 30:

/* Line 1806 of yacc.c  */
#line 209 "pmatch_parse.yy"
    {
    if ((yyvsp[(3) - (3)].replaceRule)->arrow != (yyvsp[(1) - (3)].replaceRules)->arrow) {
        pmatcherror("Replace type mismatch in parallel rules");
    }
    (yyval.replaceRules) = dynamic_cast<PmatchParallelRulesContainer *>((yyval.replaceRules));
    (yyvsp[(1) - (3)].replaceRules)->rules.push_back((yyvsp[(3) - (3)].replaceRule));
}
    break;

  case 31:

/* Line 1806 of yacc.c  */
#line 215 "pmatch_parse.yy"
    {
    (yyval.replaceRules) = new PmatchParallelRulesContainer((yyvsp[(1) - (1)].replaceRule));
}
    break;

  case 32:

/* Line 1806 of yacc.c  */
#line 220 "pmatch_parse.yy"
    { (yyval.replaceRule) = new PmatchReplaceRuleContainer((yyvsp[(1) - (1)].mappings)); }
    break;

  case 33:

/* Line 1806 of yacc.c  */
#line 222 "pmatch_parse.yy"
    { (yyval.replaceRule) = new PmatchReplaceRuleContainer((yyvsp[(1) - (2)].mappings), (yyvsp[(2) - (2)].parallelContexts)); }
    break;

  case 34:

/* Line 1806 of yacc.c  */
#line 226 "pmatch_parse.yy"
    {
          if ((yyvsp[(1) - (3)].mappings)->arrow != (yyvsp[(3) - (3)].mappings)->arrow) {
             pmatcherror("Replace type mismatch in parallel rules.");
          }
         (yyvsp[(1) - (3)].mappings)->push_back((yyvsp[(3) - (3)].mappings));
      }
    break;

  case 35:

/* Line 1806 of yacc.c  */
#line 232 "pmatch_parse.yy"
    { (yyval.mappings) = (yyvsp[(1) - (1)].mappings); }
    break;

  case 36:

/* Line 1806 of yacc.c  */
#line 235 "pmatch_parse.yy"
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[(2) - (3)].replaceArrow), (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 37:

/* Line 1806 of yacc.c  */
#line 237 "pmatch_parse.yy"
    {
    PmatchMarkupContainer * markup = new PmatchMarkupContainer((yyvsp[(3) - (5)].pmatchObject), (yyvsp[(5) - (5)].pmatchObject));
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[(2) - (5)].replaceArrow), (yyvsp[(1) - (5)].pmatchObject), markup); }
    break;

  case 38:

/* Line 1806 of yacc.c  */
#line 240 "pmatch_parse.yy"
    {
    PmatchTransducerContainer * epsilon = new PmatchTransducerContainer(
        new HfstTransducer(hfst::internal_epsilon, format));
    PmatchMarkupContainer * markup = new PmatchMarkupContainer((yyvsp[(3) - (4)].pmatchObject), epsilon);
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[(2) - (4)].replaceArrow), (yyvsp[(1) - (4)].pmatchObject), markup);
}
    break;

  case 39:

/* Line 1806 of yacc.c  */
#line 245 "pmatch_parse.yy"
    {
    PmatchMarkupContainer * markup = new PmatchMarkupContainer(new PmatchEpsilonArc, (yyvsp[(4) - (4)].pmatchObject));
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[(2) - (4)].replaceArrow), (yyvsp[(1) - (4)].pmatchObject), markup);
}
    break;

  case 40:

/* Line 1806 of yacc.c  */
#line 248 "pmatch_parse.yy"
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[(3) - (4)].replaceArrow), new PmatchEpsilonArc, (yyvsp[(4) - (4)].pmatchObject));
}
    break;

  case 41:

/* Line 1806 of yacc.c  */
#line 250 "pmatch_parse.yy"
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[(4) - (5)].replaceArrow), (yyvsp[(2) - (5)].pmatchObject), (yyvsp[(5) - (5)].pmatchObject));
}
    break;

  case 42:

/* Line 1806 of yacc.c  */
#line 252 "pmatch_parse.yy"
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[(2) - (4)].replaceArrow), (yyvsp[(1) - (4)].pmatchObject), new PmatchEpsilonArc);
}
    break;

  case 43:

/* Line 1806 of yacc.c  */
#line 254 "pmatch_parse.yy"
    {
    (yyval.mappings) = new PmatchMappingPairsContainer((yyvsp[(2) - (5)].replaceArrow), (yyvsp[(1) - (5)].pmatchObject), (yyvsp[(4) - (5)].pmatchObject)); }
    break;

  case 44:

/* Line 1806 of yacc.c  */
#line 259 "pmatch_parse.yy"
    {
    (yyval.parallelContexts) = new PmatchContextsContainer((yyvsp[(1) - (2)].replType), (yyvsp[(2) - (2)].parallelContexts));
}
    break;

  case 45:

/* Line 1806 of yacc.c  */
#line 263 "pmatch_parse.yy"
    {
    (yyval.parallelContexts) = new PmatchContextsContainer((yyvsp[(1) - (1)].parallelContexts));
}
    break;

  case 46:

/* Line 1806 of yacc.c  */
#line 265 "pmatch_parse.yy"
    {
    (yyvsp[(1) - (3)].parallelContexts)->push_back((yyvsp[(3) - (3)].parallelContexts));
    (yyval.parallelContexts) = (yyvsp[(1) - (3)].parallelContexts);
}
    break;

  case 47:

/* Line 1806 of yacc.c  */
#line 271 "pmatch_parse.yy"
    { (yyval.parallelContexts) = new PmatchContextsContainer((yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 48:

/* Line 1806 of yacc.c  */
#line 272 "pmatch_parse.yy"
    { (yyval.parallelContexts) = new PmatchContextsContainer((yyvsp[(1) - (2)].pmatchObject), new PmatchEpsilonArc); }
    break;

  case 49:

/* Line 1806 of yacc.c  */
#line 273 "pmatch_parse.yy"
    { (yyval.parallelContexts) = new PmatchContextsContainer(new PmatchEpsilonArc, (yyvsp[(2) - (2)].pmatchObject)); }
    break;

  case 50:

/* Line 1806 of yacc.c  */
#line 274 "pmatch_parse.yy"
    { (yyval.parallelContexts) = new PmatchContextsContainer(new PmatchEpsilonArc, new PmatchEpsilonArc);
}
    break;

  case 51:

/* Line 1806 of yacc.c  */
#line 278 "pmatch_parse.yy"
    { (yyval.replType) = REPL_UP; }
    break;

  case 52:

/* Line 1806 of yacc.c  */
#line 279 "pmatch_parse.yy"
    { (yyval.replType) = REPL_RIGHT; }
    break;

  case 53:

/* Line 1806 of yacc.c  */
#line 280 "pmatch_parse.yy"
    { (yyval.replType) = REPL_LEFT; }
    break;

  case 54:

/* Line 1806 of yacc.c  */
#line 281 "pmatch_parse.yy"
    { (yyval.replType) = REPL_DOWN; }
    break;

  case 55:

/* Line 1806 of yacc.c  */
#line 284 "pmatch_parse.yy"
    { (yyval.replaceArrow) = E_REPLACE_RIGHT; }
    break;

  case 56:

/* Line 1806 of yacc.c  */
#line 285 "pmatch_parse.yy"
    { (yyval.replaceArrow) = E_OPTIONAL_REPLACE_RIGHT; }
    break;

  case 57:

/* Line 1806 of yacc.c  */
#line 286 "pmatch_parse.yy"
    { (yyval.replaceArrow) = E_RTL_LONGEST_MATCH; }
    break;

  case 58:

/* Line 1806 of yacc.c  */
#line 287 "pmatch_parse.yy"
    { (yyval.replaceArrow) = E_RTL_SHORTEST_MATCH; }
    break;

  case 59:

/* Line 1806 of yacc.c  */
#line 288 "pmatch_parse.yy"
    { (yyval.replaceArrow) = E_LTR_LONGEST_MATCH; }
    break;

  case 60:

/* Line 1806 of yacc.c  */
#line 289 "pmatch_parse.yy"
    { (yyval.replaceArrow) = E_LTR_SHORTEST_MATCH; }
    break;

  case 61:

/* Line 1806 of yacc.c  */
#line 290 "pmatch_parse.yy"
    { (yyval.replaceArrow) =  E_REPLACE_LEFT; }
    break;

  case 62:

/* Line 1806 of yacc.c  */
#line 291 "pmatch_parse.yy"
    { (yyval.replaceArrow) = E_OPTIONAL_REPLACE_LEFT;
}
    break;

  case 63:

/* Line 1806 of yacc.c  */
#line 294 "pmatch_parse.yy"
    { }
    break;

  case 64:

/* Line 1806 of yacc.c  */
#line 295 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Shuffle, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 65:

/* Line 1806 of yacc.c  */
#line 296 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Before, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject));}
    break;

  case 66:

/* Line 1806 of yacc.c  */
#line 297 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(After, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 67:

/* Line 1806 of yacc.c  */
#line 299 "pmatch_parse.yy"
    { }
    break;

  case 68:

/* Line 1806 of yacc.c  */
#line 300 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchRestrictionContainer((yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].restrictionContexts)); }
    break;

  case 69:

/* Line 1806 of yacc.c  */
#line 301 "pmatch_parse.yy"
    { pmatcherror("Left arrow with contexts not implemented"); }
    break;

  case 70:

/* Line 1806 of yacc.c  */
#line 302 "pmatch_parse.yy"
    { pmatcherror("Left-right arrow with contexts not implemented"); }
    break;

  case 71:

/* Line 1806 of yacc.c  */
#line 304 "pmatch_parse.yy"
    {
    (yyval.restrictionContexts) = new MappingPairVector();
    (yyval.restrictionContexts)->push_back(*(yyvsp[(1) - (1)].restrictionContext));
    delete (yyvsp[(1) - (1)].restrictionContext);
}
    break;

  case 72:

/* Line 1806 of yacc.c  */
#line 309 "pmatch_parse.yy"
    {
     (yyvsp[(1) - (3)].restrictionContexts)->push_back(*(yyvsp[(3) - (3)].restrictionContext));
     (yyval.restrictionContexts) = (yyvsp[(1) - (3)].restrictionContexts);
     delete (yyvsp[(3) - (3)].restrictionContext);
}
    break;

  case 73:

/* Line 1806 of yacc.c  */
#line 316 "pmatch_parse.yy"
    { (yyval.restrictionContext) = new PmatchObjectPair((yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 74:

/* Line 1806 of yacc.c  */
#line 317 "pmatch_parse.yy"
    { (yyval.restrictionContext) = new PmatchObjectPair((yyvsp[(1) - (2)].pmatchObject), new PmatchEpsilonArc); }
    break;

  case 75:

/* Line 1806 of yacc.c  */
#line 318 "pmatch_parse.yy"
    { (yyval.restrictionContext) = new PmatchObjectPair(new PmatchEpsilonArc, (yyvsp[(2) - (2)].pmatchObject)); }
    break;

  case 76:

/* Line 1806 of yacc.c  */
#line 319 "pmatch_parse.yy"
    { (yyval.restrictionContext) = new PmatchObjectPair(new PmatchEmpty, new PmatchEmpty); }
    break;

  case 77:

/* Line 1806 of yacc.c  */
#line 321 "pmatch_parse.yy"
    { }
    break;

  case 78:

/* Line 1806 of yacc.c  */
#line 322 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Disjunct, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 79:

/* Line 1806 of yacc.c  */
#line 323 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Intersect, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 80:

/* Line 1806 of yacc.c  */
#line 324 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Subtract, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 81:

/* Line 1806 of yacc.c  */
#line 325 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(UpperSubtract, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 82:

/* Line 1806 of yacc.c  */
#line 326 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(LowerSubtract, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 83:

/* Line 1806 of yacc.c  */
#line 327 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(UpperPriorityUnion, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 84:

/* Line 1806 of yacc.c  */
#line 328 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(LowerPriorityUnion, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 85:

/* Line 1806 of yacc.c  */
#line 330 "pmatch_parse.yy"
    { }
    break;

  case 86:

/* Line 1806 of yacc.c  */
#line 331 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(Concatenate, (yyvsp[(1) - (2)].pmatchObject), (yyvsp[(2) - (2)].pmatchObject)); }
    break;

  case 87:

/* Line 1806 of yacc.c  */
#line 333 "pmatch_parse.yy"
    { }
    break;

  case 88:

/* Line 1806 of yacc.c  */
#line 334 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(InsertFreely, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 89:

/* Line 1806 of yacc.c  */
#line 335 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(IgnoreInternally, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 90:

/* Line 1806 of yacc.c  */
#line 336 "pmatch_parse.yy"
    { pmatcherror("Left quotient not implemented"); }
    break;

  case 91:

/* Line 1806 of yacc.c  */
#line 338 "pmatch_parse.yy"
    { }
    break;

  case 92:

/* Line 1806 of yacc.c  */
#line 339 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Complement, (yyvsp[(2) - (2)].pmatchObject)); }
    break;

  case 93:

/* Line 1806 of yacc.c  */
#line 340 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Containment, (yyvsp[(2) - (2)].pmatchObject)); }
    break;

  case 94:

/* Line 1806 of yacc.c  */
#line 341 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(ContainmentOnce, (yyvsp[(2) - (2)].pmatchObject)); }
    break;

  case 95:

/* Line 1806 of yacc.c  */
#line 342 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(ContainmentOptional, (yyvsp[(2) - (2)].pmatchObject)); }
    break;

  case 96:

/* Line 1806 of yacc.c  */
#line 344 "pmatch_parse.yy"
    { }
    break;

  case 97:

/* Line 1806 of yacc.c  */
#line 345 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(RepeatStar, (yyvsp[(1) - (2)].pmatchObject)); }
    break;

  case 98:

/* Line 1806 of yacc.c  */
#line 346 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(RepeatPlus, (yyvsp[(1) - (2)].pmatchObject)); }
    break;

  case 99:

/* Line 1806 of yacc.c  */
#line 347 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Reverse, (yyvsp[(1) - (2)].pmatchObject)); }
    break;

  case 100:

/* Line 1806 of yacc.c  */
#line 348 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Invert, (yyvsp[(1) - (2)].pmatchObject)); }
    break;

  case 101:

/* Line 1806 of yacc.c  */
#line 349 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(InputProject, (yyvsp[(1) - (2)].pmatchObject)); }
    break;

  case 102:

/* Line 1806 of yacc.c  */
#line 350 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(OutputProject, (yyvsp[(1) - (2)].pmatchObject)); }
    break;

  case 103:

/* Line 1806 of yacc.c  */
#line 351 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchNumericOperation(RepeatN, (yyvsp[(1) - (2)].pmatchObject));
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[(2) - (2)].value));
}
    break;

  case 104:

/* Line 1806 of yacc.c  */
#line 355 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchNumericOperation(RepeatNPlus, (yyvsp[(1) - (2)].pmatchObject));
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[(2) - (2)].value) + 1);
}
    break;

  case 105:

/* Line 1806 of yacc.c  */
#line 359 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchNumericOperation(RepeatNMinus, (yyvsp[(1) - (2)].pmatchObject));
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[(2) - (2)].value) - 1);
}
    break;

  case 106:

/* Line 1806 of yacc.c  */
#line 363 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchNumericOperation(RepeatNToK, (yyvsp[(1) - (2)].pmatchObject));
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[(2) - (2)].values)[0]);
    (dynamic_cast<PmatchNumericOperation *>((yyval.pmatchObject)))->values.push_back((yyvsp[(2) - (2)].values)[1]);
    free((yyvsp[(2) - (2)].values));
}
    break;

  case 107:

/* Line 1806 of yacc.c  */
#line 370 "pmatch_parse.yy"
    { }
    break;

  case 108:

/* Line 1806 of yacc.c  */
#line 371 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(TermComplement, (yyvsp[(2) - (2)].pmatchObject)); }
    break;

  case 109:

/* Line 1806 of yacc.c  */
#line 373 "pmatch_parse.yy"
    { }
    break;

  case 110:

/* Line 1806 of yacc.c  */
#line 374 "pmatch_parse.yy"
    { (yyval.pmatchObject) = (yyvsp[(2) - (3)].pmatchObject); }
    break;

  case 111:

/* Line 1806 of yacc.c  */
#line 375 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBinaryOperation(CrossProduct, (yyvsp[(1) - (3)].pmatchObject), (yyvsp[(3) - (3)].pmatchObject)); }
    break;

  case 112:

/* Line 1806 of yacc.c  */
#line 376 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Optionalize, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 113:

/* Line 1806 of yacc.c  */
#line 377 "pmatch_parse.yy"
    { (yyval.pmatchObject) = (yyvsp[(1) - (2)].pmatchObject); (yyval.pmatchObject)->weight += (yyvsp[(2) - (2)].weight); }
    break;

  case 114:

/* Line 1806 of yacc.c  */
#line 378 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchUnaryOperation(AddDelimiters,
                                  new PmatchBinaryOperation(Concatenate, (yyvsp[(2) - (6)].pmatchObject),
                                                            new PmatchString((yyvsp[(5) - (6)].label))));
    free((yyvsp[(5) - (6)].label)); }
    break;

  case 115:

/* Line 1806 of yacc.c  */
#line 383 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchUnaryOperation(AddDelimiters,
                                  new PmatchBinaryOperation(Concatenate, (yyvsp[(2) - (6)].pmatchObject),
                                                            new PmatchString((yyvsp[(5) - (6)].label))));
    free((yyvsp[(5) - (6)].label)); }
    break;

  case 116:

/* Line 1806 of yacc.c  */
#line 390 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchString(std::string((yyvsp[(1) - (1)].label))); free((yyvsp[(1) - (1)].label)); }
    break;

  case 117:

/* Line 1806 of yacc.c  */
#line 391 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchString(hfst::internal_epsilon); }
    break;

  case 118:

/* Line 1806 of yacc.c  */
#line 392 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchString("@BOUNDARY@"); }
    break;

  case 119:

/* Line 1806 of yacc.c  */
#line 393 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchString(std::string((yyvsp[(2) - (3)].label))); free((yyvsp[(2) - (3)].label)); }
    break;

  case 120:

/* Line 1806 of yacc.c  */
#line 394 "pmatch_parse.yy"
    {
    PmatchString * retval = new PmatchString(std::string((yyvsp[(1) - (1)].label)));
    retval->multichar = true;
    (yyval.pmatchObject) = retval; free((yyvsp[(1) - (1)].label));
}
    break;

  case 121:

/* Line 1806 of yacc.c  */
#line 399 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchQuestionMark; }
    break;

  case 122:

/* Line 1806 of yacc.c  */
#line 400 "pmatch_parse.yy"
    { }
    break;

  case 123:

/* Line 1806 of yacc.c  */
#line 401 "pmatch_parse.yy"
    { }
    break;

  case 124:

/* Line 1806 of yacc.c  */
#line 402 "pmatch_parse.yy"
    { }
    break;

  case 125:

/* Line 1806 of yacc.c  */
#line 404 "pmatch_parse.yy"
    { }
    break;

  case 126:

/* Line 1806 of yacc.c  */
#line 405 "pmatch_parse.yy"
    { }
    break;

  case 127:

/* Line 1806 of yacc.c  */
#line 406 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchAcceptor(Alpha); }
    break;

  case 128:

/* Line 1806 of yacc.c  */
#line 407 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchAcceptor(LowercaseAlpha); }
    break;

  case 129:

/* Line 1806 of yacc.c  */
#line 408 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchAcceptor(UppercaseAlpha); }
    break;

  case 130:

/* Line 1806 of yacc.c  */
#line 409 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchAcceptor(Numeral); }
    break;

  case 131:

/* Line 1806 of yacc.c  */
#line 410 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchAcceptor(Punctuation); }
    break;

  case 132:

/* Line 1806 of yacc.c  */
#line 411 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchAcceptor(Whitespace); }
    break;

  case 133:

/* Line 1806 of yacc.c  */
#line 412 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(Cap, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 134:

/* Line 1806 of yacc.c  */
#line 413 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(OptCap, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 135:

/* Line 1806 of yacc.c  */
#line 414 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(ToLower, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 136:

/* Line 1806 of yacc.c  */
#line 415 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(ToUpper, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 137:

/* Line 1806 of yacc.c  */
#line 416 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(OptToLower, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 138:

/* Line 1806 of yacc.c  */
#line 417 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(OptToUpper, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 139:

/* Line 1806 of yacc.c  */
#line 418 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(AnyCase, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 140:

/* Line 1806 of yacc.c  */
#line 420 "pmatch_parse.yy"
    {
    if (strcmp((yyvsp[(4) - (5)].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(CapUpper, (yyvsp[(2) - (5)].pmatchObject));
    } else if (strcmp((yyvsp[(4) - (5)].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(CapLower, (yyvsp[(2) - (5)].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(Cap, (yyvsp[(2) - (5)].pmatchObject));
    }
    free((yyvsp[(4) - (5)].label));
}
    break;

  case 141:

/* Line 1806 of yacc.c  */
#line 431 "pmatch_parse.yy"
    {
    if (strcmp((yyvsp[(4) - (5)].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptCapUpper, (yyvsp[(2) - (5)].pmatchObject));
    } else if (strcmp((yyvsp[(4) - (5)].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptCapLower, (yyvsp[(2) - (5)].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptCap, (yyvsp[(2) - (5)].pmatchObject));
    }
    free((yyvsp[(4) - (5)].label));
}
    break;

  case 142:

/* Line 1806 of yacc.c  */
#line 442 "pmatch_parse.yy"
    {
    if (strcmp((yyvsp[(4) - (5)].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToLowerUpper, (yyvsp[(2) - (5)].pmatchObject));
    } else if (strcmp((yyvsp[(4) - (5)].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToLowerLower, (yyvsp[(2) - (5)].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToLower, (yyvsp[(2) - (5)].pmatchObject));
    }
    free((yyvsp[(4) - (5)].label));
}
    break;

  case 143:

/* Line 1806 of yacc.c  */
#line 453 "pmatch_parse.yy"
    {
    if (strcmp((yyvsp[(4) - (5)].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToUpperUpper, (yyvsp[(2) - (5)].pmatchObject));
    } else if (strcmp((yyvsp[(4) - (5)].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToUpperLower, (yyvsp[(2) - (5)].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(ToUpper, (yyvsp[(2) - (5)].pmatchObject));
    }
    free((yyvsp[(4) - (5)].label));
}
    break;

  case 144:

/* Line 1806 of yacc.c  */
#line 464 "pmatch_parse.yy"
    {
    if (strcmp((yyvsp[(4) - (5)].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToLowerUpper, (yyvsp[(2) - (5)].pmatchObject));
    } else if (strcmp((yyvsp[(4) - (5)].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToLowerLower, (yyvsp[(2) - (5)].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToLower, (yyvsp[(2) - (5)].pmatchObject));
    }
    free((yyvsp[(4) - (5)].label));
}
    break;

  case 145:

/* Line 1806 of yacc.c  */
#line 475 "pmatch_parse.yy"
    {
    if (strcmp((yyvsp[(4) - (5)].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToUpperUpper, (yyvsp[(2) - (5)].pmatchObject));
    } else if (strcmp((yyvsp[(4) - (5)].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToUpperLower, (yyvsp[(2) - (5)].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(OptToUpper, (yyvsp[(2) - (5)].pmatchObject));
    }
    free((yyvsp[(4) - (5)].label));
}
    break;

  case 146:

/* Line 1806 of yacc.c  */
#line 486 "pmatch_parse.yy"
    {
    if (strcmp((yyvsp[(4) - (5)].label), "U") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(AnyCaseUpper, (yyvsp[(2) - (5)].pmatchObject));
    } else if (strcmp((yyvsp[(4) - (5)].label), "L") == 0) {
        (yyval.pmatchObject) = new PmatchUnaryOperation(AnyCaseLower, (yyvsp[(2) - (5)].pmatchObject));
    } else {
        pmatcherror("Side argument to casing function not understood\n");
        (yyval.pmatchObject) = new PmatchUnaryOperation(AnyCase, (yyvsp[(2) - (5)].pmatchObject));
    }
    free((yyvsp[(4) - (5)].label));
}
    break;

  case 147:

/* Line 1806 of yacc.c  */
#line 497 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(AddDelimiters, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 148:

/* Line 1806 of yacc.c  */
#line 498 "pmatch_parse.yy"
    { }
    break;

  case 149:

/* Line 1806 of yacc.c  */
#line 499 "pmatch_parse.yy"
    { (yyval.pmatchObject) = (yyvsp[(1) - (1)].pmatchObject); }
    break;

  case 150:

/* Line 1806 of yacc.c  */
#line 500 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(MakeList, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 151:

/* Line 1806 of yacc.c  */
#line 501 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(MakeExcList, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 152:

/* Line 1806 of yacc.c  */
#line 502 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchBuiltinFunction(Interpolate, (yyvsp[(2) - (3)].pmatchObject_vector)); }
    break;

  case 153:

/* Line 1806 of yacc.c  */
#line 503 "pmatch_parse.yy"
    { (yyval.pmatchObject) = new PmatchUnaryOperation(MakeSigma, (yyvsp[(2) - (3)].pmatchObject)); }
    break;

  case 154:

/* Line 1806 of yacc.c  */
#line 504 "pmatch_parse.yy"
    { (yyval.pmatchObject) = hfst::pmatch::make_counter((yyvsp[(2) - (3)].label)); free((yyvsp[(2) - (3)].label)); }
    break;

  case 155:

/* Line 1806 of yacc.c  */
#line 505 "pmatch_parse.yy"
    { (yyval.pmatchObject) = (yyvsp[(1) - (1)].pmatchObject); hfst::pmatch::need_delimiters = true; }
    break;

  case 156:

/* Line 1806 of yacc.c  */
#line 506 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = (yyvsp[(1) - (1)].pmatchObject);
    // We will wrap the current definition with entry and exit guards
    hfst::pmatch::need_delimiters = true;
    // Switch off the automatic separator-seeking context condition
    hfst::pmatch::variables["need-separators"] = "off";
}
    break;

  case 157:

/* Line 1806 of yacc.c  */
#line 513 "pmatch_parse.yy"
    {
    std::string sym((yyvsp[(1) - (1)].label));
    free((yyvsp[(1) - (1)].label));
    if (sym.size() == 0) {
        (yyval.pmatchObject) = new PmatchEmpty;
    } else {
        (yyval.pmatchObject) = new PmatchSymbol(sym);
        used_definitions.insert(sym);
    }
}
    break;

  case 158:

/* Line 1806 of yacc.c  */
#line 525 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchString((yyvsp[(2) - (3)].label), true);
    free((yyvsp[(2) - (3)].label));
}
    break;

  case 159:

/* Line 1806 of yacc.c  */
#line 531 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchString((yyvsp[(2) - (3)].label));
    free((yyvsp[(2) - (3)].label));
}
    break;

  case 160:

/* Line 1806 of yacc.c  */
#line 537 "pmatch_parse.yy"
    { (yyval.label) = (yyvsp[(1) - (1)].label); }
    break;

  case 161:

/* Line 1806 of yacc.c  */
#line 539 "pmatch_parse.yy"
    {
    (yyval.label) = static_cast<char*>(malloc(sizeof(char)*(strlen((yyvsp[(1) - (3)].label)) + strlen((yyvsp[(3) - (3)].label))+1)));
    strcpy((yyval.label), (yyvsp[(1) - (3)].label));
    strcat((yyval.label), (yyvsp[(3) - (3)].label));
    free((yyvsp[(1) - (3)].label)); free((yyvsp[(3) - (3)].label));
}
    break;

  case 162:

/* Line 1806 of yacc.c  */
#line 547 "pmatch_parse.yy"
    {
    std::string sym((yyvsp[(1) - (3)].label));
    if (function_names.count((yyvsp[(1) - (3)].label)) == 0) {
        std::stringstream ss;
        ss << "Function " << sym << " hasn't been defined\n";
        pmatcherror(ss.str().c_str());
        (yyval.pmatchObject) = new PmatchString("");
    } else {
        (yyval.pmatchObject) = new PmatchFuncall(
            (yyvsp[(2) - (3)].pmatchObject_vector),
            dynamic_cast<PmatchFunction *>(symbol_from_global_context(sym)));
    }
    used_definitions.insert(sym);
    free((yyvsp[(1) - (3)].label));
}
    break;

  case 163:

/* Line 1806 of yacc.c  */
#line 563 "pmatch_parse.yy"
    {
(yyval.pmatchObject_vector) = (yyvsp[(3) - (3)].pmatchObject_vector); (yyval.pmatchObject_vector)->push_back((yyvsp[(1) - (3)].pmatchObject)); }
    break;

  case 164:

/* Line 1806 of yacc.c  */
#line 565 "pmatch_parse.yy"
    { (yyval.pmatchObject_vector) = new std::vector<PmatchObject *>(1, (yyvsp[(1) - (1)].pmatchObject)); }
    break;

  case 165:

/* Line 1806 of yacc.c  */
#line 566 "pmatch_parse.yy"
    { (yyval.pmatchObject_vector) = new std::vector<PmatchObject *>; }
    break;

  case 166:

/* Line 1806 of yacc.c  */
#line 568 "pmatch_parse.yy"
    {
    if (!hfst::pmatch::flatten) {
        if(hfst::pmatch::definitions.count((yyvsp[(2) - (3)].label)) == 0) {
            hfst::pmatch::unsatisfied_insertions.insert((yyvsp[(2) - (3)].label));
        }
        (yyval.pmatchObject) = new PmatchString(hfst::pmatch::get_Ins_transition((yyvsp[(2) - (3)].label)));
        hfst::pmatch::inserted_names.insert((yyvsp[(2) - (3)].label));
        hfst::pmatch::used_definitions.insert((yyvsp[(2) - (3)].label));
    } else if(hfst::pmatch::definitions.count((yyvsp[(2) - (3)].label)) != 0) {
        (yyval.pmatchObject) = hfst::pmatch::definitions[(yyvsp[(2) - (3)].label)];
    } else {
        (yyval.pmatchObject) = new PmatchEmpty;
        std::stringstream ss;
        ss << "Insertion of " << (yyvsp[(2) - (3)].label) << " on line " << pmatchlineno << " is undefined and --flatten is in use\n";
        pmatcherror(ss.str().c_str());
    }
    free((yyvsp[(2) - (3)].label));
}
    break;

  case 167:

/* Line 1806 of yacc.c  */
#line 587 "pmatch_parse.yy"
    {
    if ((yyvsp[(2) - (3)].string_vector)->size() == 0) {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc("");
    } else if ((yyvsp[(2) - (3)].string_vector)->size() == 1) {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[(2) - (3)].string_vector)->operator[](0));
    } else {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[(2) - (3)].string_vector)->operator[](0),
                                            (yyvsp[(2) - (3)].string_vector)->operator[](1));
    }
    delete((yyvsp[(2) - (3)].string_vector));
}
    break;

  case 168:

/* Line 1806 of yacc.c  */
#line 598 "pmatch_parse.yy"
    {
    if ((yyvsp[(2) - (4)].string_vector)->size() == 0) {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc("");
    } else if ((yyvsp[(2) - (4)].string_vector)->size() == 1) {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[(2) - (4)].string_vector)->operator[](0), "", (yyvsp[(4) - (4)].value));
    } else {
        (yyval.pmatchObject) = hfst::pmatch::compile_like_arc((yyvsp[(2) - (4)].string_vector)->operator[](0),
                                            (yyvsp[(2) - (4)].string_vector)->operator[](1), (yyvsp[(4) - (4)].value));
    }
    delete((yyvsp[(2) - (4)].string_vector));
}
    break;

  case 169:

/* Line 1806 of yacc.c  */
#line 610 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = hfst::pmatch::make_end_tag((yyvsp[(2) - (3)].label));
    free((yyvsp[(2) - (3)].label));
}
    break;

  case 170:

/* Line 1806 of yacc.c  */
#line 613 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = hfst::pmatch::make_end_tag((yyvsp[(2) - (3)].label));
    free((yyvsp[(2) - (3)].label));
}
    break;

  case 171:

/* Line 1806 of yacc.c  */
#line 618 "pmatch_parse.yy"
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[(1) - (1)].label));
    free((yyvsp[(1) - (1)].label));
    HfstTransducer * read = NULL;
    try {
        hfst::HfstInputStream instream(filepath);
        read = new HfstTransducer(instream);
        instream.close();
    } catch(HfstException) {
        std::string ermsg =
            std::string("Couldn't read transducer from ") +
            filepath;
        pmatcherror(ermsg.c_str());
    }
    if (read->get_type() != hfst::pmatch::format) {
        read->convert(hfst::pmatch::format);
    }
    (yyval.pmatchObject) = new PmatchTransducerContainer(read);
}
    break;

  case 172:

/* Line 1806 of yacc.c  */
#line 636 "pmatch_parse.yy"
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[(1) - (1)].label));
    free((yyvsp[(1) - (1)].label));
    (yyval.pmatchObject) = new PmatchTransducerContainer(hfst::pmatch::read_text(filepath));
}
    break;

  case 173:

/* Line 1806 of yacc.c  */
#line 640 "pmatch_parse.yy"
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[(1) - (1)].label));
    free((yyvsp[(1) - (1)].label));
    (yyval.pmatchObject) = new PmatchTransducerContainer(hfst::pmatch::read_spaced_text(filepath));
}
    break;

  case 174:

/* Line 1806 of yacc.c  */
#line 644 "pmatch_parse.yy"
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[(1) - (1)].label));
    free((yyvsp[(1) - (1)].label));
    FILE * f = NULL;
    f = hfst::hfst_fopen(filepath.c_str(), "r");
    if (f == NULL) {
        pmatcherror("File cannot be opened.\n");
    } else {
        try {
            unsigned int linecount = 0;
            HfstBasicTransducer tmp = HfstBasicTransducer::read_in_prolog_format(f, linecount);
            fclose(f);
            HfstTransducer * t = new HfstTransducer(tmp, hfst::pmatch::format);
            t->minimize();
            (yyval.pmatchObject) = new PmatchTransducerContainer(t);
        }
        catch (const HfstException & e) {
            (void) e;
            fclose(f);
            pmatcherror("Error reading prolog file.\n");
        }
    }
}
    break;

  case 175:

/* Line 1806 of yacc.c  */
#line 666 "pmatch_parse.yy"
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[(1) - (1)].label));
    free((yyvsp[(1) - (1)].label));
    (yyval.pmatchObject) = new PmatchTransducerContainer(hfst::HfstTransducer::read_lexc_ptr(filepath, format, hfst::pmatch::verbose));
}
    break;

  case 176:

/* Line 1806 of yacc.c  */
#line 670 "pmatch_parse.yy"
    {
    std::string filepath = hfst::pmatch::path_from_filename((yyvsp[(1) - (1)].label));
    free((yyvsp[(1) - (1)].label));
    std::string regex;
    std::string tmp;
    std::ifstream regexfile(filepath);
    if (regexfile.is_open()) {
        while (getline(regexfile, tmp)) {
            regex.append(tmp);
        }
    }
    if (regex.size() == 0) {
        std::stringstream err;
        err << "Failed to read regex from " << filepath << ".\n";
        pmatcherror(err.str().c_str());
    }
    hfst::xre::XreCompiler xre_compiler;
    (yyval.pmatchObject) = new PmatchTransducerContainer(xre_compiler.compile(regex));
    }
    break;

  case 177:

/* Line 1806 of yacc.c  */
#line 691 "pmatch_parse.yy"
    { }
    break;

  case 178:

/* Line 1806 of yacc.c  */
#line 692 "pmatch_parse.yy"
    { }
    break;

  case 179:

/* Line 1806 of yacc.c  */
#line 693 "pmatch_parse.yy"
    { }
    break;

  case 180:

/* Line 1806 of yacc.c  */
#line 696 "pmatch_parse.yy"
    { }
    break;

  case 181:

/* Line 1806 of yacc.c  */
#line 697 "pmatch_parse.yy"
    { }
    break;

  case 182:

/* Line 1806 of yacc.c  */
#line 698 "pmatch_parse.yy"
    { }
    break;

  case 183:

/* Line 1806 of yacc.c  */
#line 699 "pmatch_parse.yy"
    { }
    break;

  case 184:

/* Line 1806 of yacc.c  */
#line 702 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = NULL;
    for (std::vector<PmatchObject *>::reverse_iterator it = (yyvsp[(2) - (3)].pmatchObject_vector)->rbegin();
         it != (yyvsp[(2) - (3)].pmatchObject_vector)->rend(); ++it) {
        if ((yyval.pmatchObject) == NULL) {
            (yyval.pmatchObject) = *it;
        } else {
            PmatchObject * tmp = (yyval.pmatchObject);
            (yyval.pmatchObject) = new PmatchBinaryOperation(Disjunct, tmp, *it);
        }
    }
    delete (yyvsp[(2) - (3)].pmatchObject_vector);
    // Zero the counter for making minimization
    // guards for disjuncted negative contexts
    hfst::pmatch::zero_minimization_guard();
}
    break;

  case 185:

/* Line 1806 of yacc.c  */
#line 720 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = NULL;
    for (std::vector<PmatchObject *>::reverse_iterator it = (yyvsp[(2) - (3)].pmatchObject_vector)->rbegin();
         it != (yyvsp[(2) - (3)].pmatchObject_vector)->rend(); ++it) {
        if ((yyval.pmatchObject) == NULL) {
            (yyval.pmatchObject) = *it;
        } else {
            PmatchObject * tmp = (yyval.pmatchObject);
            (yyval.pmatchObject) = new PmatchBinaryOperation(Concatenate, tmp, *it);
        }
    }
    delete (yyvsp[(2) - (3)].pmatchObject_vector);
}
    break;

  case 186:

/* Line 1806 of yacc.c  */
#line 735 "pmatch_parse.yy"
    {
    (yyval.pmatchObject_vector) = new std::vector<PmatchObject *>(1, (yyvsp[(1) - (1)].pmatchObject));
}
    break;

  case 187:

/* Line 1806 of yacc.c  */
#line 738 "pmatch_parse.yy"
    {
    (yyvsp[(3) - (3)].pmatchObject_vector)->push_back((yyvsp[(1) - (3)].pmatchObject));
    (yyval.pmatchObject_vector) = (yyvsp[(3) - (3)].pmatchObject_vector);
}
    break;

  case 188:

/* Line 1806 of yacc.c  */
#line 743 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchBinaryOperation(Concatenate, make_rc_entry(),
                                   new PmatchBinaryOperation(
                                       Concatenate, (yyvsp[(2) - (3)].pmatchObject), make_rc_exit()));
}
    break;

  case 189:

/* Line 1806 of yacc.c  */
#line 749 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchBinaryOperation(
        Concatenate, make_minimization_guard(),
        new PmatchBinaryOperation(
            Disjunct, make_passthrough(),
            new PmatchBinaryOperation(
                Concatenate, make_nrc_entry(),
                new PmatchBinaryOperation(Concatenate, (yyvsp[(2) - (3)].pmatchObject), make_nrc_exit()))));
}
    break;

  case 190:

/* Line 1806 of yacc.c  */
#line 759 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchBinaryOperation(
        Concatenate, make_lc_entry(),
        new PmatchBinaryOperation(
            Concatenate, new PmatchUnaryOperation(
                Reverse, (yyvsp[(2) - (3)].pmatchObject)), make_lc_exit()));
}
    break;

  case 191:

/* Line 1806 of yacc.c  */
#line 767 "pmatch_parse.yy"
    {
    (yyval.pmatchObject) = new PmatchBinaryOperation(
        Concatenate, make_minimization_guard(),
        new PmatchBinaryOperation(
            Disjunct, make_passthrough(),
            new PmatchBinaryOperation(
                Concatenate, make_nlc_entry(),
                new PmatchBinaryOperation(Concatenate, new PmatchUnaryOperation(
                                              Reverse, (yyvsp[(2) - (3)].pmatchObject)), make_nlc_exit()))));
}
    break;



/* Line 1806 of yacc.c  */
#line 3958 "pmatch_parse.cc"
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
		      yytoken, &yylval);
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


      yydestruct ("Error: popping",
		  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  *++yyvsp = yylval;


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
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule which action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
		  yystos[*yyssp], yyvsp);
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
#line 806 "pmatch_parse.yy"


