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
#define YYPURE 1

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1

/* Using locations.  */
#define YYLSP_NEEDED 0

/* Substitute the variable and function names.  */
#define yyparse         xreparse
#define yylex           xrelex
#define yyerror         xreerror
#define yylval          xrelval
#define yychar          xrechar
#define yydebug         xredebug
#define yynerrs         xrenerrs


/* Copy the first part of user declarations.  */

/* Line 268 of yacc.c  */
#line 1 "xre_parse.yy"

// Copyright (c) 2016 University of Helsinki
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 3 of the License, or (at your option) any later version.
// See the file COPYING included with this distribution for more
// information.

#define YYDEBUG 1

#include <stdio.h>
#include <assert.h>
#include <iostream>

#include "HfstTransducer.h"
#include "HfstInputStream.h"
#include "HfstXeroxRules.h"

using namespace hfst;
using hfst::HfstTransducer;
using namespace hfst::xeroxRules;
using namespace hfst::implementations;

#include "xre_utils.h"

namespace hfst {
  namespace xre {
    // number of characters read, used for scanning function definition xre for argument symbols
    extern unsigned int cr;
    extern bool harmonize_;
    extern bool harmonize_flags_;
    extern bool allow_extra_text_at_end;

    bool has_weight_been_zeroed = false; // to control how many times a warning is given
    float zero_weights(float f)
    {
        if ((! has_weight_been_zeroed) && (f != 0))
        {
            hfst::xre::warn("warning: ignoring weights in rule context\n");
            has_weight_been_zeroed = true;
        }
        return 0;
    }

    bool is_weighted()
    {
        return (hfst::xre::format == hfst::TROPICAL_OPENFST_TYPE ||
                hfst::xre::format == hfst::LOG_OPENFST_TYPE);
    }
  }
}

using hfst::xre::harmonize_;
using hfst::xre::harmonize_flags_;

union YYSTYPE;
struct yy_buffer_state;
typedef yy_buffer_state * YY_BUFFER_STATE;
typedef void * yyscan_t;

extern int xreparse(yyscan_t);
extern int xrelex_init (yyscan_t*);
extern YY_BUFFER_STATE xre_scan_string (const char *, yyscan_t);
extern void xre_delete_buffer (YY_BUFFER_STATE, yyscan_t);
extern int xrelex_destroy (yyscan_t);

extern int xreerror(yyscan_t, const char*);
extern int xreerror(const char*);
int xrelex ( YYSTYPE * , yyscan_t );



/* Line 268 of yacc.c  */
#line 154 "xre_parse.cc"

/* Enabling traces.  */
#ifndef YYDEBUG
# define YYDEBUG 1
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
     CURLY_BRACKETS = 259,
     MULTICHAR_SYMBOL = 260,
     SYMBOL = 261,
     MERGE_LEFT_ARROW = 262,
     MERGE_RIGHT_ARROW = 263,
     INTERSECTION = 264,
     LENIENT_COMPOSITION = 265,
     COMPOSITION = 266,
     CROSS_PRODUCT = 267,
     MARKUP_MARKER = 268,
     CENTER_MARKER = 269,
     SHUFFLE = 270,
     LEFT_RIGHT_ARROW = 271,
     RIGHT_ARROW = 272,
     LEFT_ARROW = 273,
     LEFT_RESTRICTION = 274,
     LTR_SHORTEST_MATCH = 275,
     LTR_LONGEST_MATCH = 276,
     RTL_SHORTEST_MATCH = 277,
     RTL_LONGEST_MATCH = 278,
     OPTIONAL_REPLACE_LEFT_RIGHT = 279,
     REPLACE_LEFT_RIGHT = 280,
     OPTIONAL_REPLACE_LEFT = 281,
     OPTIONAL_REPLACE_RIGHT = 282,
     REPLACE_LEFT = 283,
     REPLACE_RIGHT = 284,
     REPLACE_CONTEXT_LL = 285,
     REPLACE_CONTEXT_UL = 286,
     REPLACE_CONTEXT_LU = 287,
     REPLACE_CONTEXT_UU = 288,
     LOWER_PRIORITY_UNION = 289,
     UPPER_PRIORITY_UNION = 290,
     LOWER_MINUS = 291,
     UPPER_MINUS = 292,
     MINUS = 293,
     UNION = 294,
     LEFT_QUOTIENT = 295,
     IGNORE_INTERNALLY = 296,
     IGNORING = 297,
     COMMACOMMA = 298,
     COMMA = 299,
     AFTER = 300,
     BEFORE = 301,
     TERM_COMPLEMENT = 302,
     SUBSTITUTE_LEFT = 303,
     CONTAINMENT_OPT = 304,
     CONTAINMENT_ONCE = 305,
     CONTAINMENT = 306,
     COMPLEMENT = 307,
     PLUS = 308,
     STAR = 309,
     XRE_LOWER = 310,
     XRE_UPPER = 311,
     INVERT = 312,
     REVERSE = 313,
     CATENATE_N_TO_K = 314,
     CATENATE_N_MINUS = 315,
     CATENATE_N_PLUS = 316,
     CATENATE_N = 317,
     READ_RE = 318,
     READ_PROLOG = 319,
     READ_SPACED = 320,
     READ_TEXT = 321,
     READ_BIN = 322,
     FUNCTION_NAME = 323,
     LEFT_BRACKET = 324,
     RIGHT_BRACKET = 325,
     LEFT_PARENTHESIS = 326,
     RIGHT_PARENTHESIS = 327,
     LEFT_BRACKET_DOTTED = 328,
     RIGHT_BRACKET_DOTTED = 329,
     SUBVAL = 330,
     EPSILON_TOKEN = 331,
     ANY_TOKEN = 332,
     BOUNDARY_MARKER = 333,
     LEXER_ERROR = 334,
     END_OF_EXPRESSION = 335,
     PAIR_SEPARATOR = 336,
     QUOTED_MULTICHAR_LITERAL = 337,
     QUOTED_LITERAL = 338
   };
#endif
/* Tokens.  */
#define WEIGHT 258
#define CURLY_BRACKETS 259
#define MULTICHAR_SYMBOL 260
#define SYMBOL 261
#define MERGE_LEFT_ARROW 262
#define MERGE_RIGHT_ARROW 263
#define INTERSECTION 264
#define LENIENT_COMPOSITION 265
#define COMPOSITION 266
#define CROSS_PRODUCT 267
#define MARKUP_MARKER 268
#define CENTER_MARKER 269
#define SHUFFLE 270
#define LEFT_RIGHT_ARROW 271
#define RIGHT_ARROW 272
#define LEFT_ARROW 273
#define LEFT_RESTRICTION 274
#define LTR_SHORTEST_MATCH 275
#define LTR_LONGEST_MATCH 276
#define RTL_SHORTEST_MATCH 277
#define RTL_LONGEST_MATCH 278
#define OPTIONAL_REPLACE_LEFT_RIGHT 279
#define REPLACE_LEFT_RIGHT 280
#define OPTIONAL_REPLACE_LEFT 281
#define OPTIONAL_REPLACE_RIGHT 282
#define REPLACE_LEFT 283
#define REPLACE_RIGHT 284
#define REPLACE_CONTEXT_LL 285
#define REPLACE_CONTEXT_UL 286
#define REPLACE_CONTEXT_LU 287
#define REPLACE_CONTEXT_UU 288
#define LOWER_PRIORITY_UNION 289
#define UPPER_PRIORITY_UNION 290
#define LOWER_MINUS 291
#define UPPER_MINUS 292
#define MINUS 293
#define UNION 294
#define LEFT_QUOTIENT 295
#define IGNORE_INTERNALLY 296
#define IGNORING 297
#define COMMACOMMA 298
#define COMMA 299
#define AFTER 300
#define BEFORE 301
#define TERM_COMPLEMENT 302
#define SUBSTITUTE_LEFT 303
#define CONTAINMENT_OPT 304
#define CONTAINMENT_ONCE 305
#define CONTAINMENT 306
#define COMPLEMENT 307
#define PLUS 308
#define STAR 309
#define XRE_LOWER 310
#define XRE_UPPER 311
#define INVERT 312
#define REVERSE 313
#define CATENATE_N_TO_K 314
#define CATENATE_N_MINUS 315
#define CATENATE_N_PLUS 316
#define CATENATE_N 317
#define READ_RE 318
#define READ_PROLOG 319
#define READ_SPACED 320
#define READ_TEXT 321
#define READ_BIN 322
#define FUNCTION_NAME 323
#define LEFT_BRACKET 324
#define RIGHT_BRACKET 325
#define LEFT_PARENTHESIS 326
#define RIGHT_PARENTHESIS 327
#define LEFT_BRACKET_DOTTED 328
#define RIGHT_BRACKET_DOTTED 329
#define SUBVAL 330
#define EPSILON_TOKEN 331
#define ANY_TOKEN 332
#define BOUNDARY_MARKER 333
#define LEXER_ERROR 334
#define END_OF_EXPRESSION 335
#define PAIR_SEPARATOR 336
#define QUOTED_MULTICHAR_LITERAL 337
#define QUOTED_LITERAL 338




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 293 of yacc.c  */
#line 82 "xre_parse.yy"


    int value;
    int* values;
    double weight;
    char* label;
    
    char *subval1, *subval2;
    
    hfst::HfstTransducer* transducer;
    hfst::HfstTransducerPair* transducerPair;
    hfst::HfstTransducerPairVector* transducerPairVector;
    hfst::HfstTransducerVector* transducerVector;

   std::pair<hfst::xeroxRules::ReplaceArrow, std::vector<hfst::xeroxRules::Rule> >* replaceRuleVectorWithArrow;
   std::pair< hfst::xeroxRules::ReplaceArrow, hfst::xeroxRules::Rule>* replaceRuleWithArrow;
   std::pair< hfst::xeroxRules::ReplaceArrow, hfst::HfstTransducerPairVector>* mappingVectorWithArrow;
   std::pair< hfst::xeroxRules::ReplaceArrow, hfst::HfstTransducerPair>* mappingWithArrow;
       
   std::pair<hfst::xeroxRules::ReplaceType, hfst::HfstTransducerPairVector>* contextWithMark;
   
   hfst::xeroxRules::ReplaceType replType;
   hfst::xeroxRules::ReplaceArrow replaceArrow;




/* Line 293 of yacc.c  */
#line 384 "xre_parse.cc"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif


/* Copy the second part of user declarations.  */


/* Line 343 of yacc.c  */
#line 396 "xre_parse.cc"

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
#define YYFINAL  59
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   649

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  84
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  35
/* YYNRULES -- Number of rules.  */
#define YYNRULES  135
/* YYNRULES -- Number of states.  */
#define YYNSTATES  214

/* YYTRANSLATE(YYLEX) -- Bison symbol number corresponding to YYLEX.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   338

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
      75,    76,    77,    78,    79,    80,    81,    82,    83
};

#if YYDEBUG
/* YYPRHS[YYN] -- Index of the first RHS symbol of rule number YYN in
   YYRHS.  */
static const yytype_uint16 yyprhs[] =
{
       0,     0,     3,     5,     6,     9,    11,    13,    17,    21,
      25,    29,    33,    43,    47,    52,    55,    58,    60,    62,
      64,    68,    70,    72,    75,    79,    81,    85,    91,    96,
     101,   106,   112,   117,   123,   126,   128,   132,   136,   139,
     142,   144,   146,   148,   150,   152,   154,   156,   158,   160,
     162,   164,   166,   168,   170,   174,   178,   182,   184,   188,
     194,   200,   202,   206,   210,   213,   216,   218,   220,   224,
     228,   232,   236,   240,   244,   248,   250,   253,   255,   259,
     263,   267,   269,   272,   275,   279,   282,   285,   287,   290,
     293,   296,   299,   302,   305,   308,   311,   314,   317,   319,
     322,   324,   328,   336,   342,   348,   354,   360,   365,   369,
     371,   374,   376,   379,   381,   383,   385,   387,   389,   391,
     395,   399,   403,   405,   409,   413,   415,   417,   419,   421,
     423,   425,   427,   429,   433,   435
};

/* YYRHS -- A `-1'-separated list of the rules' RHS.  */
static const yytype_int8 yyrhs[] =
{
      85,     0,    -1,    86,    -1,    -1,    87,    80,    -1,    87,
      -1,    91,    -1,    87,    11,    91,    -1,    87,    12,    91,
      -1,    87,    10,    91,    -1,    87,     8,    91,    -1,    87,
       7,    91,    -1,    88,   116,    81,   116,    44,   116,    81,
     116,    70,    -1,    88,    89,    90,    -1,    48,    69,    91,
      44,    -1,   116,    44,    -1,   112,    70,    -1,    70,    -1,
     101,    -1,    92,    -1,    92,    43,    93,    -1,    93,    -1,
      94,    -1,    94,    96,    -1,    94,    44,    95,    -1,    95,
      -1,    91,   100,    91,    -1,    91,   100,    91,    13,    91,
      -1,    91,   100,    91,    13,    -1,    91,   100,    13,    91,
      -1,    73,    74,   100,    91,    -1,    73,    91,    74,   100,
      91,    -1,    91,   100,    73,    74,    -1,    91,   100,    73,
      91,    74,    -1,    99,    97,    -1,    98,    -1,    97,    44,
      98,    -1,    91,    14,    91,    -1,    91,    14,    -1,    14,
      91,    -1,    14,    -1,    33,    -1,    32,    -1,    31,    -1,
      30,    -1,    29,    -1,    27,    -1,    23,    -1,    22,    -1,
      21,    -1,    20,    -1,    28,    -1,    26,    -1,   102,    -1,
     101,    15,   102,    -1,   101,    46,   102,    -1,   101,    45,
     102,    -1,   105,    -1,   102,    17,   103,    -1,   102,    18,
     105,    14,   105,    -1,   102,    16,   105,    14,   105,    -1,
     104,    -1,   103,    44,   104,    -1,   102,    14,   102,    -1,
     102,    14,    -1,    14,   102,    -1,    14,    -1,   106,    -1,
     105,    39,   106,    -1,   105,     9,   106,    -1,   105,    38,
     106,    -1,   105,    37,   106,    -1,   105,    36,   106,    -1,
     105,    35,   106,    -1,   105,    34,   106,    -1,   107,    -1,
     106,   107,    -1,   108,    -1,   107,    42,   108,    -1,   107,
      41,   108,    -1,   107,    40,   108,    -1,   109,    -1,    52,
     108,    -1,    51,   108,    -1,    51,     3,   108,    -1,    50,
     108,    -1,    49,   108,    -1,   110,    -1,   109,    54,    -1,
     109,    53,    -1,   109,    58,    -1,   109,    57,    -1,   109,
      56,    -1,   109,    55,    -1,   109,    62,    -1,   109,    61,
      -1,   109,    60,    -1,   109,    59,    -1,   111,    -1,    47,
     110,    -1,   113,    -1,    69,    87,    70,    -1,    69,    87,
      70,    81,    69,    87,    70,    -1,    69,    87,    70,    81,
       4,    -1,     4,    81,    69,    87,    70,    -1,    69,    87,
      70,    81,   116,    -1,   116,    81,    69,    87,    70,    -1,
      69,    87,    70,     3,    -1,    71,    87,    72,    -1,   116,
      -1,   112,   116,    -1,   114,    -1,   114,     3,    -1,    67,
      -1,    66,    -1,    65,    -1,    64,    -1,    63,    -1,   116,
      -1,   116,    81,   116,    -1,   116,    81,     4,    -1,     4,
      81,   116,    -1,     4,    -1,     4,    81,     4,    -1,   118,
     117,    72,    -1,     6,    -1,     5,    -1,    82,    -1,    83,
      -1,   115,    -1,    76,    -1,    77,    -1,    78,    -1,   117,
      44,    87,    -1,    87,    -1,    68,    -1
};

/* YYRLINE[YYN] -- source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   174,   174,   176,   182,   189,   196,   200,   225,   229,
     233,   247,   252,   257,   335,   336,   337,   339,   346,   347,
     386,   399,   411,   420,   432,   449,   462,   471,   480,   490,
     500,   510,   517,   525,   535,   541,   549,   557,   590,   612,
     635,   641,   645,   649,   653,   659,   663,   667,   671,   675,
     679,   683,   687,   694,   695,   701,   705,   712,   714,   720,
     728,   737,   745,   754,   759,   769,   775,   783,   784,   788,
     793,   797,   803,   809,   813,   823,   824,   830,   831,   837,
     843,   851,   852,   860,   873,   883,   889,   895,   896,   899,
     902,   905,   908,   911,   914,   917,   921,   924,   930,   931,
     946,   947,   951,   956,   963,   970,   977,   983,   986,   992,
    1003,  1021,  1022,  1025,  1041,  1066,  1091,  1116,  1162,  1176,
    1181,  1189,  1197,  1201,  1207,  1257,  1258,  1262,  1266,  1269,
    1278,  1281,  1284,  1289,  1293,  1300
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || YYTOKEN_TABLE
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "WEIGHT", "CURLY_BRACKETS",
  "MULTICHAR_SYMBOL", "SYMBOL", "MERGE_LEFT_ARROW", "MERGE_RIGHT_ARROW",
  "INTERSECTION", "LENIENT_COMPOSITION", "COMPOSITION", "CROSS_PRODUCT",
  "MARKUP_MARKER", "CENTER_MARKER", "SHUFFLE", "LEFT_RIGHT_ARROW",
  "RIGHT_ARROW", "LEFT_ARROW", "LEFT_RESTRICTION", "LTR_SHORTEST_MATCH",
  "LTR_LONGEST_MATCH", "RTL_SHORTEST_MATCH", "RTL_LONGEST_MATCH",
  "OPTIONAL_REPLACE_LEFT_RIGHT", "REPLACE_LEFT_RIGHT",
  "OPTIONAL_REPLACE_LEFT", "OPTIONAL_REPLACE_RIGHT", "REPLACE_LEFT",
  "REPLACE_RIGHT", "REPLACE_CONTEXT_LL", "REPLACE_CONTEXT_UL",
  "REPLACE_CONTEXT_LU", "REPLACE_CONTEXT_UU", "LOWER_PRIORITY_UNION",
  "UPPER_PRIORITY_UNION", "LOWER_MINUS", "UPPER_MINUS", "MINUS", "UNION",
  "LEFT_QUOTIENT", "IGNORE_INTERNALLY", "IGNORING", "COMMACOMMA", "COMMA",
  "AFTER", "BEFORE", "TERM_COMPLEMENT", "SUBSTITUTE_LEFT",
  "CONTAINMENT_OPT", "CONTAINMENT_ONCE", "CONTAINMENT", "COMPLEMENT",
  "PLUS", "STAR", "XRE_LOWER", "XRE_UPPER", "INVERT", "REVERSE",
  "CATENATE_N_TO_K", "CATENATE_N_MINUS", "CATENATE_N_PLUS", "CATENATE_N",
  "READ_RE", "READ_PROLOG", "READ_SPACED", "READ_TEXT", "READ_BIN",
  "FUNCTION_NAME", "LEFT_BRACKET", "RIGHT_BRACKET", "LEFT_PARENTHESIS",
  "RIGHT_PARENTHESIS", "LEFT_BRACKET_DOTTED", "RIGHT_BRACKET_DOTTED",
  "SUBVAL", "EPSILON_TOKEN", "ANY_TOKEN", "BOUNDARY_MARKER", "LEXER_ERROR",
  "END_OF_EXPRESSION", "PAIR_SEPARATOR", "QUOTED_MULTICHAR_LITERAL",
  "QUOTED_LITERAL", "$accept", "XRE", "REGEXP1", "REGEXP2", "SUB1", "SUB2",
  "SUB3", "REPLACE", "PARALLEL_RULES", "RULE", "MAPPINGPAIR_VECTOR",
  "MAPPINGPAIR", "CONTEXTS_WITH_MARK", "CONTEXTS_VECTOR", "CONTEXT",
  "CONTEXT_MARK", "REPLACE_ARROW", "REGEXP3", "REGEXP4",
  "RESTR_CONTEXTS_VECTOR", "RESTR_CONTEXT", "REGEXP5", "REGEXP6",
  "REGEXP7", "REGEXP8", "REGEXP9", "REGEXP10", "REGEXP11", "SYMBOL_LIST",
  "REGEXP12", "LABEL", "SYMBOL_OR_QUOTED", "HALFARC", "REGEXP_LIST",
  "FUNCTION", 0
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
     335,   336,   337,   338
};
# endif

/* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    84,    85,    85,    86,    86,    87,    87,    87,    87,
      87,    87,    87,    87,    88,    89,    90,    90,    91,    91,
      92,    92,    93,    93,    94,    94,    95,    95,    95,    95,
      95,    95,    95,    95,    96,    97,    97,    98,    98,    98,
      98,    99,    99,    99,    99,   100,   100,   100,   100,   100,
     100,   100,   100,   101,   101,   101,   101,   102,   102,   102,
     102,   103,   103,   104,   104,   104,   104,   105,   105,   105,
     105,   105,   105,   105,   105,   106,   106,   107,   107,   107,
     107,   108,   108,   108,   108,   108,   108,   109,   109,   109,
     109,   109,   109,   109,   109,   109,   109,   109,   110,   110,
     111,   111,   111,   111,   111,   111,   111,   111,   111,   112,
     112,   113,   113,   113,   113,   113,   113,   113,   114,   114,
     114,   114,   114,   114,   114,   115,   115,   115,   115,   116,
     116,   116,   116,   117,   117,   118
};

/* YYR2[YYN] -- Number of symbols composing right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     0,     2,     1,     1,     3,     3,     3,
       3,     3,     9,     3,     4,     2,     2,     1,     1,     1,
       3,     1,     1,     2,     3,     1,     3,     5,     4,     4,
       4,     5,     4,     5,     2,     1,     3,     3,     2,     2,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     3,     3,     3,     1,     3,     5,
       5,     1,     3,     3,     2,     2,     1,     1,     3,     3,
       3,     3,     3,     3,     3,     1,     2,     1,     3,     3,
       3,     1,     2,     2,     3,     2,     2,     1,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     1,     2,
       1,     3,     7,     5,     5,     5,     5,     4,     3,     1,
       2,     1,     2,     1,     1,     1,     1,     1,     1,     3,
       3,     3,     1,     3,     3,     1,     1,     1,     1,     1,
       1,     1,     1,     3,     1,     1
};

/* YYDEFACT[STATE-NAME] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE doesn't specify something else to do.  Zero
   means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       3,   122,   126,   125,     0,     0,     0,     0,     0,     0,
     117,   116,   115,   114,   113,   135,     0,     0,     0,   130,
     131,   132,   127,   128,     0,     2,     5,     0,     6,    19,
      21,    22,    25,    18,    53,    57,    67,    75,    77,    81,
      87,    98,   100,   111,   129,   118,     0,     0,    99,     0,
      86,    85,     0,    83,    82,     0,     0,     0,     0,     1,
       0,     0,     0,     0,     0,     4,     0,     0,    50,    49,
      48,    47,    52,    46,    51,    45,     0,     0,    44,    43,
      42,    41,     0,    23,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,    76,     0,
       0,     0,    89,    88,    93,    92,    91,    90,    97,    96,
      95,    94,   112,     0,   134,     0,   123,     0,   121,     0,
      84,   101,   108,     0,     0,    11,    10,     9,     7,     8,
      17,    13,     0,   109,    15,     0,     0,     0,    26,     0,
      20,    24,    40,     0,    34,    35,    54,    56,    55,     0,
      66,     0,    58,    61,     0,    69,    74,    73,    72,    71,
      70,    68,    80,    79,    78,   120,     0,   119,     0,   124,
       0,    14,   107,     0,    30,     0,    16,   110,     0,    29,
      32,     0,    28,    39,    38,     0,     0,    65,    64,     0,
       0,     0,   133,   104,   103,     0,   105,    31,     0,    33,
      27,    37,    36,    60,    63,    62,    59,   106,     0,     0,
     102,     0,     0,    12
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,    24,    25,    26,    27,    66,   131,    28,    29,    30,
      31,    32,    83,   144,   145,    84,    76,    33,    34,   152,
     153,    35,    36,    37,    38,    39,    40,    41,   132,    42,
      43,    44,    45,   115,    46
};

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
#define YYPACT_NINF -123
static const yytype_int16 yypact[] =
{
     173,   -70,  -123,  -123,    13,   -54,   478,   478,   136,   478,
    -123,  -123,  -123,  -123,  -123,  -123,   173,   173,   211,  -123,
    -123,  -123,  -123,  -123,    30,  -123,    33,    16,   613,   -11,
    -123,   124,  -123,    21,    11,   542,   478,   155,  -123,   570,
    -123,  -123,  -123,    32,  -123,   -65,   173,   310,  -123,   385,
    -123,  -123,   478,  -123,  -123,   182,    47,   613,   100,  -123,
     385,   385,   385,   385,   385,  -123,    82,   -35,  -123,  -123,
    -123,  -123,  -123,  -123,  -123,  -123,   260,   385,  -123,  -123,
    -123,  -123,   385,  -123,   299,   478,   478,   478,   478,   441,
     478,   478,   478,   478,   478,   478,   478,   478,   155,   478,
     478,   478,  -123,  -123,  -123,  -123,  -123,  -123,  -123,  -123,
    -123,  -123,  -123,   397,   137,   -34,  -123,   173,  -123,   566,
    -123,    31,  -123,   385,   613,   613,   613,   613,   613,   613,
    -123,  -123,   492,  -123,  -123,    16,   385,   348,   577,   613,
    -123,  -123,   385,   593,    -2,  -123,    11,    11,    11,   283,
     478,   192,     3,  -123,   371,   478,   478,   478,   478,   478,
     478,   478,  -123,  -123,  -123,  -123,   173,  -123,   173,  -123,
     220,  -123,  -123,   481,   613,   385,  -123,  -123,     9,   613,
     613,   511,   385,   613,   385,   299,   478,    11,   478,   441,
     478,   288,   137,  -123,  -123,   173,  -123,   613,    16,   613,
     613,   613,  -123,   542,    11,  -123,   542,  -123,   431,   -48,
    -123,    16,   -14,  -123
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -123,  -123,  -123,   -15,  -123,  -123,  -123,   -12,  -123,   -16,
    -123,   -20,  -123,  -123,  -122,  -123,   -49,  -123,   -82,  -123,
    -118,   -76,   552,   -23,    17,  -123,    69,  -123,  -123,  -123,
    -123,  -123,   -27,  -123,  -123
};

/* YYTABLE[YYPACT[STATE-NUM]].  What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule which
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
#define YYTABLE_NINF -1
static const yytype_uint8 yytable[] =
{
      67,    55,    56,   146,   147,   148,    58,   151,   123,   134,
     168,    47,   149,    98,   154,    49,   113,     1,     2,     3,
     118,     2,     3,    50,    51,    53,    54,    88,    89,    90,
      59,   114,    77,   211,   172,   112,    85,   119,   169,   133,
      60,    61,   185,    62,    63,    64,   135,   189,   125,   126,
     127,   128,   129,   198,    60,    61,   213,    62,    63,    64,
       4,   140,   141,   202,   138,   139,    86,    87,   187,   120,
     139,   205,   143,    48,     0,   175,    10,    11,    12,    13,
      14,    15,    16,     0,    17,     0,   167,     2,     3,    19,
      20,    21,    19,    20,    21,    22,    23,     0,    22,    23,
       0,     0,   170,     0,     0,   177,   204,   151,   178,     0,
     203,   174,   173,    65,   206,     0,   162,   163,   164,   122,
      68,    69,    70,    71,   179,   181,    72,    73,    74,    75,
     183,   123,    98,    98,    98,    98,    98,    98,    98,    52,
       1,     2,     3,     0,    60,    61,   196,    62,    63,    64,
     175,   191,   130,   192,    78,    79,    80,    81,    19,    20,
      21,     0,     0,   197,    22,    23,     0,     0,    82,     0,
     200,   209,   201,   143,   124,     0,     0,     1,     2,     3,
     208,     0,     0,     4,   212,     6,     7,     8,     9,    60,
      61,     0,    62,    63,    64,    99,   100,   101,     0,    10,
      11,    12,    13,    14,    15,    16,   188,    17,    88,    89,
      90,     0,    19,    20,    21,     1,     2,     3,    22,    23,
       4,     5,     6,     7,     8,     9,     0,    60,    61,     0,
      62,    63,    64,     0,     0,     0,    10,    11,    12,    13,
      14,    15,    16,     0,    17,     0,    18,     0,     0,    19,
      20,    21,   121,     0,     0,    22,    23,     0,     4,     0,
       6,     7,     8,     9,     1,     2,     3,     0,     0,     0,
       0,     0,     0,   136,    10,    11,    12,    13,    14,    15,
      16,     0,    17,     0,    18,    57,     0,    19,    20,    21,
     193,     0,    91,    22,    23,    60,    61,   186,    62,    63,
      64,     0,     0,     1,     2,     3,     0,     4,     0,     6,
       7,     8,     9,   142,   116,     2,     3,    92,    93,    94,
      95,    96,    97,    10,    11,    12,    13,    14,    15,    16,
       0,    17,     0,   137,     0,     0,    19,    20,    21,     0,
       0,     0,    22,    23,     0,     0,     4,     0,     6,     7,
       8,     9,     1,     2,     3,     0,     0,     0,   207,     0,
       0,     0,    10,    11,    12,    13,    14,    15,    16,     0,
      17,     0,    18,     0,     0,    19,    20,    21,     0,   117,
      91,    22,    23,     0,     0,   190,    19,    20,    21,     1,
       2,     3,    22,    23,     0,     4,     0,     6,     7,     8,
       9,   165,     2,     3,     0,    92,    93,    94,    95,    96,
      97,    10,    11,    12,    13,    14,    15,    16,     0,    17,
       0,    18,   180,     0,    19,    20,    21,     0,     0,     0,
      22,    23,     4,     0,     6,     7,     8,     9,    60,    61,
       0,    62,    63,    64,     0,     1,     2,     3,    10,    11,
      12,    13,    14,    15,    16,   150,    17,     0,    18,     0,
       0,    19,    20,    21,     0,     0,   166,    22,    23,     0,
       0,     0,     0,    19,    20,    21,     0,     0,     0,    22,
      23,     0,     1,     2,     3,   194,     2,     3,     4,     0,
       6,     7,     8,     9,     0,     0,     0,     2,     3,     0,
       0,   210,     0,     0,    10,    11,    12,    13,    14,    15,
      16,     0,    17,     0,     0,     0,     0,    19,    20,    21,
       0,     0,     0,    22,    23,     4,     0,     6,     7,     8,
       9,    68,    69,    70,    71,     0,     0,    72,    73,    74,
      75,    10,    11,    12,    13,    14,    15,    16,     0,    17,
     195,    91,     0,     0,    19,    20,    21,    19,    20,    21,
      22,    23,   176,    22,    23,     0,     0,     0,    19,    20,
      21,     0,     0,     0,    22,    23,    92,    93,    94,    95,
      96,    97,     0,     0,     0,   199,    68,    69,    70,    71,
     182,     0,    72,    73,    74,    75,     0,    68,    69,    70,
      71,     0,     0,    72,    73,    74,    75,   184,     0,     0,
     171,     0,     0,    68,    69,    70,    71,     0,     0,    72,
      73,    74,    75,   102,   103,   104,   105,   106,   107,   108,
     109,   110,   111,    68,    69,    70,    71,     0,     0,    72,
      73,    74,    75,   155,   156,   157,   158,   159,   160,   161
};

#define yypact_value_is_default(yystate) \
  ((yystate) == (-123))

#define yytable_value_is_error(yytable_value) \
  YYID (0)

static const yytype_int16 yycheck[] =
{
      27,    16,    17,    85,    86,    87,    18,    89,    57,    44,
      44,    81,    88,    36,    90,    69,    81,     4,     5,     6,
      47,     5,     6,     6,     7,     8,     9,    16,    17,    18,
       0,    46,    43,    81,     3,     3,    15,    49,    72,    66,
       7,     8,    44,    10,    11,    12,    81,    44,    60,    61,
      62,    63,    64,    44,     7,     8,    70,    10,    11,    12,
      47,    77,    82,   185,    76,    77,    45,    46,   150,    52,
      82,   189,    84,     4,    -1,   124,    63,    64,    65,    66,
      67,    68,    69,    -1,    71,    -1,   113,     5,     6,    76,
      77,    78,    76,    77,    78,    82,    83,    -1,    82,    83,
      -1,    -1,   117,    -1,    -1,   132,   188,   189,   135,    -1,
     186,   123,    81,    80,   190,    -1,    99,   100,   101,    72,
      20,    21,    22,    23,   136,   137,    26,    27,    28,    29,
     142,   180,   155,   156,   157,   158,   159,   160,   161,     3,
       4,     5,     6,    -1,     7,     8,   173,    10,    11,    12,
     199,   166,    70,   168,    30,    31,    32,    33,    76,    77,
      78,    -1,    -1,   175,    82,    83,    -1,    -1,    44,    -1,
     182,   198,   184,   185,    74,    -1,    -1,     4,     5,     6,
     195,    -1,    -1,    47,   211,    49,    50,    51,    52,     7,
       8,    -1,    10,    11,    12,    40,    41,    42,    -1,    63,
      64,    65,    66,    67,    68,    69,    14,    71,    16,    17,
      18,    -1,    76,    77,    78,     4,     5,     6,    82,    83,
      47,    48,    49,    50,    51,    52,    -1,     7,     8,    -1,
      10,    11,    12,    -1,    -1,    -1,    63,    64,    65,    66,
      67,    68,    69,    -1,    71,    -1,    73,    -1,    -1,    76,
      77,    78,    70,    -1,    -1,    82,    83,    -1,    47,    -1,
      49,    50,    51,    52,     4,     5,     6,    -1,    -1,    -1,
      -1,    -1,    -1,    13,    63,    64,    65,    66,    67,    68,
      69,    -1,    71,    -1,    73,    74,    -1,    76,    77,    78,
      70,    -1,     9,    82,    83,     7,     8,    14,    10,    11,
      12,    -1,    -1,     4,     5,     6,    -1,    47,    -1,    49,
      50,    51,    52,    14,     4,     5,     6,    34,    35,    36,
      37,    38,    39,    63,    64,    65,    66,    67,    68,    69,
      -1,    71,    -1,    73,    -1,    -1,    76,    77,    78,    -1,
      -1,    -1,    82,    83,    -1,    -1,    47,    -1,    49,    50,
      51,    52,     4,     5,     6,    -1,    -1,    -1,    70,    -1,
      -1,    -1,    63,    64,    65,    66,    67,    68,    69,    -1,
      71,    -1,    73,    -1,    -1,    76,    77,    78,    -1,    69,
       9,    82,    83,    -1,    -1,    14,    76,    77,    78,     4,
       5,     6,    82,    83,    -1,    47,    -1,    49,    50,    51,
      52,     4,     5,     6,    -1,    34,    35,    36,    37,    38,
      39,    63,    64,    65,    66,    67,    68,    69,    -1,    71,
      -1,    73,    74,    -1,    76,    77,    78,    -1,    -1,    -1,
      82,    83,    47,    -1,    49,    50,    51,    52,     7,     8,
      -1,    10,    11,    12,    -1,     4,     5,     6,    63,    64,
      65,    66,    67,    68,    69,    14,    71,    -1,    73,    -1,
      -1,    76,    77,    78,    -1,    -1,    69,    82,    83,    -1,
      -1,    -1,    -1,    76,    77,    78,    -1,    -1,    -1,    82,
      83,    -1,     4,     5,     6,     4,     5,     6,    47,    -1,
      49,    50,    51,    52,    -1,    -1,    -1,     5,     6,    -1,
      -1,    70,    -1,    -1,    63,    64,    65,    66,    67,    68,
      69,    -1,    71,    -1,    -1,    -1,    -1,    76,    77,    78,
      -1,    -1,    -1,    82,    83,    47,    -1,    49,    50,    51,
      52,    20,    21,    22,    23,    -1,    -1,    26,    27,    28,
      29,    63,    64,    65,    66,    67,    68,    69,    -1,    71,
      69,     9,    -1,    -1,    76,    77,    78,    76,    77,    78,
      82,    83,    70,    82,    83,    -1,    -1,    -1,    76,    77,
      78,    -1,    -1,    -1,    82,    83,    34,    35,    36,    37,
      38,    39,    -1,    -1,    -1,    74,    20,    21,    22,    23,
      13,    -1,    26,    27,    28,    29,    -1,    20,    21,    22,
      23,    -1,    -1,    26,    27,    28,    29,    14,    -1,    -1,
      44,    -1,    -1,    20,    21,    22,    23,    -1,    -1,    26,
      27,    28,    29,    53,    54,    55,    56,    57,    58,    59,
      60,    61,    62,    20,    21,    22,    23,    -1,    -1,    26,
      27,    28,    29,    91,    92,    93,    94,    95,    96,    97
};

/* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
   symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     4,     5,     6,    47,    48,    49,    50,    51,    52,
      63,    64,    65,    66,    67,    68,    69,    71,    73,    76,
      77,    78,    82,    83,    85,    86,    87,    88,    91,    92,
      93,    94,    95,   101,   102,   105,   106,   107,   108,   109,
     110,   111,   113,   114,   115,   116,   118,    81,   110,    69,
     108,   108,     3,   108,   108,    87,    87,    74,    91,     0,
       7,     8,    10,    11,    12,    80,    89,   116,    20,    21,
      22,    23,    26,    27,    28,    29,   100,    43,    30,    31,
      32,    33,    44,    96,    99,    15,    45,    46,    16,    17,
      18,     9,    34,    35,    36,    37,    38,    39,   107,    40,
      41,    42,    53,    54,    55,    56,    57,    58,    59,    60,
      61,    62,     3,    81,    87,   117,     4,    69,   116,    91,
     108,    70,    72,   100,    74,    91,    91,    91,    91,    91,
      70,    90,   112,   116,    44,    81,    13,    73,    91,    91,
      93,    95,    14,    91,    97,    98,   102,   102,   102,   105,
      14,   102,   103,   104,   105,   106,   106,   106,   106,   106,
     106,   106,   108,   108,   108,     4,    69,   116,    44,    72,
      87,    44,     3,    81,    91,   100,    70,   116,   116,    91,
      74,    91,    13,    91,    14,    44,    14,   102,    14,    44,
      14,    87,    87,    70,     4,    69,   116,    91,    44,    74,
      91,    91,    98,   105,   102,   104,   105,    70,    87,   116,
      70,    81,   116,    70
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
      yyerror (scanner, YY_("syntax error: cannot back up")); \
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
# define YYLEX yylex (&yylval, YYLEX_PARAM)
#else
# define YYLEX yylex (&yylval, scanner)
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
		  Type, Value, scanner); \
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
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, void * scanner)
#else
static void
yy_symbol_value_print (yyoutput, yytype, yyvaluep, scanner)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
    void * scanner;
#endif
{
  if (!yyvaluep)
    return;
  YYUSE (scanner);
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
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep, void * scanner)
#else
static void
yy_symbol_print (yyoutput, yytype, yyvaluep, scanner)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
    void * scanner;
#endif
{
  if (yytype < YYNTOKENS)
    YYFPRINTF (yyoutput, "token %s (", yytname[yytype]);
  else
    YYFPRINTF (yyoutput, "nterm %s (", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep, scanner);
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
yy_reduce_print (YYSTYPE *yyvsp, int yyrule, void * scanner)
#else
static void
yy_reduce_print (yyvsp, yyrule, scanner)
    YYSTYPE *yyvsp;
    int yyrule;
    void * scanner;
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
		       		       , scanner);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)		\
do {					\
  if (yydebug)				\
    yy_reduce_print (yyvsp, Rule, scanner); \
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
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep, void * scanner)
#else
static void
yydestruct (yymsg, yytype, yyvaluep, scanner)
    const char *yymsg;
    int yytype;
    YYSTYPE *yyvaluep;
    void * scanner;
#endif
{
  YYUSE (yyvaluep);
  YYUSE (scanner);

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
int yyparse (void * scanner);
#else
int yyparse ();
#endif
#endif /* ! YYPARSE_PARAM */


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
yyparse (void * scanner)
#else
int
yyparse (scanner)
    void * scanner;
#endif
#endif
{
/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;

    /* Number of syntax errors so far.  */
    int yynerrs;

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
        case 2:

/* Line 1806 of yacc.c  */
#line 174 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 3:

/* Line 1806 of yacc.c  */
#line 176 "xre_parse.yy"
    {
       // only comments
       hfst::xre::contains_only_comments = true;
       return 0;
     }
    break;

  case 4:

/* Line 1806 of yacc.c  */
#line 182 "xre_parse.yy"
    {
       hfst::xre::last_compiled = (yyvsp[(1) - (2)].transducer);
       (yyval.transducer) = hfst::xre::last_compiled;
       if (hfst::xre::allow_extra_text_at_end) {
         return 0;
       }
   }
    break;

  case 5:

/* Line 1806 of yacc.c  */
#line 189 "xre_parse.yy"
    {
        hfst::xre::last_compiled = (yyvsp[(1) - (1)].transducer);
        (yyval.transducer) = hfst::xre::last_compiled;
   }
    break;

  case 6:

/* Line 1806 of yacc.c  */
#line 197 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (1)].transducer)->optimize();
         }
    break;

  case 7:

/* Line 1806 of yacc.c  */
#line 201 "xre_parse.yy"
    {
        if ((yyvsp[(1) - (3)].transducer)->has_flag_diacritics() && (yyvsp[(3) - (3)].transducer)->has_flag_diacritics())
          {
            if (! harmonize_flags_) {
                 hfst::xre::warn("warning: both composition arguments contain flag diacritics that are not harmonized\n");
            }
            else {
                (yyvsp[(1) - (3)].transducer)->harmonize_flag_diacritics(*(yyvsp[(3) - (3)].transducer));
            }
          }

         try {
            (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->compose(*(yyvsp[(3) - (3)].transducer), harmonize_).optimize();
         }
         catch (const FlagDiacriticsAreNotIdentitiesException & e)
             {
               (void)e;
               xreerror("Error: flag diacritics must be identities in composition if flag-is-epsilon is ON.\n"
               "I.e. only FLAG:FLAG is allowed, not FLAG1:FLAG2, FLAG:bar or foo:FLAG\n"
               "Apply twosided flag-diacritics (tfd) before composition.\n");
               YYABORT;
             }
            delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 8:

/* Line 1806 of yacc.c  */
#line 225 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->cross_product(*(yyvsp[(3) - (3)].transducer)).optimize();
            delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 9:

/* Line 1806 of yacc.c  */
#line 229 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->lenient_composition(*(yyvsp[(3) - (3)].transducer)).optimize();
            delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 10:

/* Line 1806 of yacc.c  */
#line 233 "xre_parse.yy"
    {
          try {
            (yyval.transducer) = & hfst::xre::merge_first_to_second((yyvsp[(1) - (3)].transducer), (yyvsp[(3) - (3)].transducer))->optimize();
          }
          catch (const TransducersAreNotAutomataException & e)
          {
            (void)e;
            xreerror("Error: transducers must be automata in merge operation.");
            delete (yyvsp[(1) - (3)].transducer);
            delete (yyvsp[(3) - (3)].transducer);
            YYABORT;
          }
          delete (yyvsp[(1) - (3)].transducer);
       }
    break;

  case 11:

/* Line 1806 of yacc.c  */
#line 247 "xre_parse.yy"
    {
            (yyval.transducer) = & hfst::xre::merge_first_to_second((yyvsp[(3) - (3)].transducer), (yyvsp[(1) - (3)].transducer))->optimize();
            delete (yyvsp[(3) - (3)].transducer);
       }
    break;

  case 12:

/* Line 1806 of yacc.c  */
#line 252 "xre_parse.yy"
    {
            (yyvsp[(1) - (9)].transducer)->substitute(StringPair((yyvsp[(2) - (9)].label),(yyvsp[(4) - (9)].label)), StringPair((yyvsp[(6) - (9)].label),(yyvsp[(8) - (9)].label)));
            (yyval.transducer) = & (yyvsp[(1) - (9)].transducer)->optimize();
            free((yyvsp[(2) - (9)].label)); free((yyvsp[(4) - (9)].label)); free((yyvsp[(6) - (9)].label)); free((yyvsp[(8) - (9)].label));
       }
    break;

  case 13:

/* Line 1806 of yacc.c  */
#line 257 "xre_parse.yy"
    {

            StringSet alpha = (yyvsp[(1) - (3)].transducer)->get_alphabet();
            if (hfst::xre::is_definition((yyvsp[(2) - (3)].label)))
            {
                hfst::xre::warn("warning: using definition as an ordinary label, cannot substitute\n");
                (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->optimize();
            }
            else if (alpha.find((yyvsp[(2) - (3)].label)) == alpha.end())
            {
                (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->optimize();
            }
            else
            {
                alpha = (yyvsp[(3) - (3)].transducer)->get_alphabet();

                StringPair tmp((yyvsp[(2) - (3)].label), (yyvsp[(2) - (3)].label));
                HfstTransducer * tmpTr = new HfstTransducer(*(yyvsp[(1) - (3)].transducer));

	        bool empty_replace_transducer=false;
	        HfstTransducer empty(hfst::xre::format);
	        if (empty.compare(*(yyvsp[(3) - (3)].transducer)))
	        {
                        empty_replace_transducer=true;
	        }

	        if (empty_replace_transducer)
	        {
                        // substitute all transitions {b:a, a:b, b:b} with b:b
		        // as they will be removed anyway
		        hfst::xre::set_substitution_function_symbol((yyvsp[(2) - (3)].label));
		        tmpTr->substitute(&hfst::xre::substitution_function);
	        }

                // `[ a:b, b, x y ]
                // substitute b with x | y
                tmpTr->substitute(tmp, *(yyvsp[(3) - (3)].transducer), false); // no harmonization

	        if (!empty_replace_transducer)
                {
                        // a:b .o. b -> x | y
                        // [[a:b].i .o. b -> x | y].i - this is for cases when b is on left side

	                // build Replace transducer
                        HfstTransducerPair mappingPair(HfstTransducer((yyvsp[(2) - (3)].label), (yyvsp[(2) - (3)].label), hfst::xre::format), *(yyvsp[(3) - (3)].transducer));
                        HfstTransducerPairVector mappingPairVector;
                        mappingPairVector.push_back(mappingPair);
                        Rule rule(mappingPairVector);
                        HfstTransducer replaceTr(hfst::xre::format);
                        replaceTr = replace(rule, false);

                        // if we are replacing with flag diacritics, the rule must allow
                        // flags to be replaced with themselves
                        StringSet alpha = (yyvsp[(3) - (3)].transducer)->get_alphabet();
                        for (StringSet::const_iterator it = alpha.begin(); it != alpha.end(); it++)
                        {
                          if (FdOperation::is_diacritic(*it))
                          {
                            replaceTr.insert_freely(StringPair(*it, *it), false);
                          }
                        }
                        replaceTr.optimize();

                        tmpTr->compose(replaceTr).optimize();
                        tmpTr->invert().compose(replaceTr).invert();
	        }
            
                if (alpha.find((yyvsp[(2) - (3)].label)) == alpha.end())
                {
                  tmpTr->remove_from_alphabet((yyvsp[(2) - (3)].label));
                }
                tmpTr->optimize();
                (yyval.transducer) = tmpTr;
                delete (yyvsp[(1) - (3)].transducer); delete (yyvsp[(2) - (3)].label); delete (yyvsp[(3) - (3)].transducer);
            }
         }
    break;

  case 14:

/* Line 1806 of yacc.c  */
#line 335 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(3) - (4)].transducer); }
    break;

  case 15:

/* Line 1806 of yacc.c  */
#line 336 "xre_parse.yy"
    { (yyval.label) = (yyvsp[(1) - (2)].label); }
    break;

  case 16:

/* Line 1806 of yacc.c  */
#line 337 "xre_parse.yy"
    {  (yyval.transducer) = (yyvsp[(1) - (2)].transducer);  }
    break;

  case 17:

/* Line 1806 of yacc.c  */
#line 339 "xre_parse.yy"
    { (yyval.transducer) = new HfstTransducer(hfst::xre::format); }
    break;

  case 18:

/* Line 1806 of yacc.c  */
#line 346 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 19:

/* Line 1806 of yacc.c  */
#line 348 "xre_parse.yy"
    {
            switch ( (yyvsp[(1) - (1)].replaceRuleVectorWithArrow)->first )
            {
               case E_REPLACE_RIGHT:
                 (yyval.transducer) = new HfstTransducer( replace( (yyvsp[(1) - (1)].replaceRuleVectorWithArrow)->second, false ) );
                 break;
               case E_OPTIONAL_REPLACE_RIGHT:
                 (yyval.transducer) = new HfstTransducer( replace( (yyvsp[(1) - (1)].replaceRuleVectorWithArrow)->second, true ) );
                 break;
              case E_REPLACE_LEFT:
                 (yyval.transducer) = new HfstTransducer( replace_left( (yyvsp[(1) - (1)].replaceRuleVectorWithArrow)->second, false ) );
                 break;
               case E_OPTIONAL_REPLACE_LEFT:
                 (yyval.transducer) = new HfstTransducer( replace_left( (yyvsp[(1) - (1)].replaceRuleVectorWithArrow)->second, true ) );
                 break;
               case E_RTL_LONGEST_MATCH:
                 (yyval.transducer) = new HfstTransducer( replace_rightmost_longest_match( (yyvsp[(1) - (1)].replaceRuleVectorWithArrow)->second ) );
                 break;
               case E_RTL_SHORTEST_MATCH:
                 (yyval.transducer) = new HfstTransducer( replace_rightmost_shortest_match((yyvsp[(1) - (1)].replaceRuleVectorWithArrow)->second) );
                 break;
               case E_LTR_LONGEST_MATCH:
                 (yyval.transducer) = new HfstTransducer( replace_leftmost_longest_match( (yyvsp[(1) - (1)].replaceRuleVectorWithArrow)->second ) );
                 break;
               case E_LTR_SHORTEST_MATCH:
                 (yyval.transducer) = new HfstTransducer( replace_leftmost_shortest_match( (yyvsp[(1) - (1)].replaceRuleVectorWithArrow)->second ) );
                 break;
               case E_REPLACE_RIGHT_MARKUP:
               default:
                xreerror("Unhandled arrow stuff I suppose");
                YYABORT;
                break;
            }
       
            delete (yyvsp[(1) - (1)].replaceRuleVectorWithArrow);
         }
    break;

  case 20:

/* Line 1806 of yacc.c  */
#line 387 "xre_parse.yy"
    {
           //std::cerr << "parallel_rules: parallel_rules ,, rule"<< std::endl;
           if ((yyvsp[(3) - (3)].replaceRuleWithArrow)->first != (yyvsp[(1) - (3)].replaceRuleVectorWithArrow)->first)
           {
             xreerror("Replace type mismatch in parallel rules");
             YYABORT;
           }
            Rule tmpRule((yyvsp[(3) - (3)].replaceRuleWithArrow)->second);
            (yyvsp[(1) - (3)].replaceRuleVectorWithArrow)->second.push_back(tmpRule);
            (yyval.replaceRuleVectorWithArrow) =  new std::pair< ReplaceArrow, std::vector<Rule> > ((yyvsp[(3) - (3)].replaceRuleWithArrow)->first, (yyvsp[(1) - (3)].replaceRuleVectorWithArrow)->second);
            delete (yyvsp[(1) - (3)].replaceRuleVectorWithArrow); delete (yyvsp[(3) - (3)].replaceRuleWithArrow);
         }
    break;

  case 21:

/* Line 1806 of yacc.c  */
#line 400 "xre_parse.yy"
    {
         //std::cerr << "parallel_rules:rule"<< std::endl;
            std::vector<Rule> * ruleVector = new std::vector<Rule>();
            ruleVector->push_back((yyvsp[(1) - (1)].replaceRuleWithArrow)->second);
            
            (yyval.replaceRuleVectorWithArrow) =  new std::pair< ReplaceArrow, std::vector<Rule> > ((yyvsp[(1) - (1)].replaceRuleWithArrow)->first, *ruleVector);
            delete ruleVector;
            delete (yyvsp[(1) - (1)].replaceRuleWithArrow);
         }
    break;

  case 22:

/* Line 1806 of yacc.c  */
#line 412 "xre_parse.yy"
    {
         // std::cerr << "rule: mapping_vector"<< std::endl;
        // HfstTransducer allMappingsDisjuncted = disjunctVectorMembers($1->second);
         
         Rule rule( (yyvsp[(1) - (1)].mappingVectorWithArrow)->second );;
         (yyval.replaceRuleWithArrow) =  new std::pair< ReplaceArrow, Rule> ((yyvsp[(1) - (1)].mappingVectorWithArrow)->first, rule);
         delete (yyvsp[(1) - (1)].mappingVectorWithArrow);
      }
    break;

  case 23:

/* Line 1806 of yacc.c  */
#line 421 "xre_parse.yy"
    {
       //  std::cerr << "rule: mapping_vector contextsWM"<< std::endl;
     //   HfstTransducer allMappingsDisjuncted = disjunctVectorMembers($1->second);
        
        Rule rule( (yyvsp[(1) - (2)].mappingVectorWithArrow)->second, (yyvsp[(2) - (2)].contextWithMark)->second, (yyvsp[(2) - (2)].contextWithMark)->first );
        (yyval.replaceRuleWithArrow) =  new std::pair< ReplaceArrow, Rule> ((yyvsp[(1) - (2)].mappingVectorWithArrow)->first, rule);
        delete (yyvsp[(1) - (2)].mappingVectorWithArrow); delete (yyvsp[(2) - (2)].contextWithMark);
      }
    break;

  case 24:

/* Line 1806 of yacc.c  */
#line 433 "xre_parse.yy"
    {
        // std::cerr << "mapping_vector : mapping_vector comma mapping"<< std::endl;
         // check if new Arrow is the same as the first one

         if ((yyvsp[(1) - (3)].mappingVectorWithArrow)->first != (yyvsp[(3) - (3)].mappingWithArrow)->first)
         {
            hfst::xre::warn("Replace arrows should be the same. Calculated as if all replacements had the first arrow.");
            //exit(1);
         }
 
         (yyvsp[(1) - (3)].mappingVectorWithArrow)->second.push_back((yyvsp[(3) - (3)].mappingWithArrow)->second);
         (yyval.mappingVectorWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPairVector> ((yyvsp[(1) - (3)].mappingVectorWithArrow)->first, (yyvsp[(1) - (3)].mappingVectorWithArrow)->second);
         delete (yyvsp[(1) - (3)].mappingVectorWithArrow); delete (yyvsp[(3) - (3)].mappingWithArrow);
            
      }
    break;

  case 25:

/* Line 1806 of yacc.c  */
#line 450 "xre_parse.yy"
    {
         // std::cerr << "mapping_vector : mapping"<< std::endl;
         HfstTransducerPairVector * mappingPairVector = new HfstTransducerPairVector();
         mappingPairVector->push_back( (yyvsp[(1) - (1)].mappingWithArrow)->second );
         (yyval.mappingVectorWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPairVector> ((yyvsp[(1) - (1)].mappingWithArrow)->first, * mappingPairVector);
         delete mappingPairVector;
         delete (yyvsp[(1) - (1)].mappingWithArrow);
      }
    break;

  case 26:

/* Line 1806 of yacc.c  */
#line 463 "xre_parse.yy"
    {
	  hfst::xre::warn_about_special_symbols_in_replace((yyvsp[(1) - (3)].transducer));
	  hfst::xre::warn_about_special_symbols_in_replace((yyvsp[(3) - (3)].transducer));
          HfstTransducerPair mappingPair(*(yyvsp[(1) - (3)].transducer), *(yyvsp[(3) - (3)].transducer));
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[(2) - (3)].replaceArrow), mappingPair);

          delete (yyvsp[(1) - (3)].transducer); delete (yyvsp[(3) - (3)].transducer);
      }
    break;

  case 27:

/* Line 1806 of yacc.c  */
#line 472 "xre_parse.yy"
    {
          HfstTransducerPair marks(*(yyvsp[(3) - (5)].transducer), *(yyvsp[(5) - (5)].transducer));
          HfstTransducerPair tmpMappingPair(*(yyvsp[(1) - (5)].transducer), HfstTransducer(hfst::xre::format));
          HfstTransducerPair mappingPair = create_mapping_for_mark_up_replace( tmpMappingPair, marks );
          
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[(2) - (5)].replaceArrow), mappingPair);
          delete (yyvsp[(1) - (5)].transducer); delete (yyvsp[(3) - (5)].transducer); delete (yyvsp[(5) - (5)].transducer);
      }
    break;

  case 28:

/* Line 1806 of yacc.c  */
#line 481 "xre_parse.yy"
    {
          HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
          HfstTransducerPair marks(*(yyvsp[(3) - (4)].transducer), epsilon);
          HfstTransducerPair tmpMappingPair(*(yyvsp[(1) - (4)].transducer), HfstTransducer(hfst::xre::format));
          HfstTransducerPair mappingPair = create_mapping_for_mark_up_replace( tmpMappingPair, marks );
                   
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[(2) - (4)].replaceArrow), mappingPair);
          delete (yyvsp[(1) - (4)].transducer); delete (yyvsp[(3) - (4)].transducer);
      }
    break;

  case 29:

/* Line 1806 of yacc.c  */
#line 491 "xre_parse.yy"
    {
          HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
          HfstTransducerPair marks(epsilon, *(yyvsp[(4) - (4)].transducer));
          HfstTransducerPair tmpMappingPair(*(yyvsp[(1) - (4)].transducer), HfstTransducer(hfst::xre::format));
          HfstTransducerPair mappingPair = create_mapping_for_mark_up_replace( tmpMappingPair, marks );
          
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[(2) - (4)].replaceArrow), mappingPair);
          delete (yyvsp[(1) - (4)].transducer); delete (yyvsp[(4) - (4)].transducer);
      }
    break;

  case 30:

/* Line 1806 of yacc.c  */
#line 501 "xre_parse.yy"
    {
          HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
          //HfstTransducer mappingTr(epsilon);
          //mappingTr.cross_product(*$4);
          HfstTransducerPair mappingPair(epsilon, *(yyvsp[(4) - (4)].transducer));
          
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[(3) - (4)].replaceArrow), mappingPair);
          delete (yyvsp[(4) - (4)].transducer);
      }
    break;

  case 31:

/* Line 1806 of yacc.c  */
#line 511 "xre_parse.yy"
    {
	  HfstTransducerPair mappingPair(*(yyvsp[(2) - (5)].transducer), *(yyvsp[(5) - (5)].transducer));
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[(4) - (5)].replaceArrow), mappingPair);
          delete (yyvsp[(2) - (5)].transducer); delete (yyvsp[(5) - (5)].transducer);
      }
    break;

  case 32:

/* Line 1806 of yacc.c  */
#line 518 "xre_parse.yy"
    {
          HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
          HfstTransducerPair mappingPair(*(yyvsp[(1) - (4)].transducer), epsilon);
          
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[(2) - (4)].replaceArrow), mappingPair);
          delete (yyvsp[(1) - (4)].transducer);
      }
    break;

  case 33:

/* Line 1806 of yacc.c  */
#line 526 "xre_parse.yy"
    {
          HfstTransducerPair mappingPair(*(yyvsp[(1) - (5)].transducer), *(yyvsp[(4) - (5)].transducer));
          (yyval.mappingWithArrow) =  new std::pair< ReplaceArrow, HfstTransducerPair> ((yyvsp[(2) - (5)].replaceArrow), mappingPair);
          delete (yyvsp[(1) - (5)].transducer); delete (yyvsp[(4) - (5)].transducer);
      }
    break;

  case 34:

/* Line 1806 of yacc.c  */
#line 536 "xre_parse.yy"
    {
         (yyval.contextWithMark) =  new std::pair< ReplaceType, HfstTransducerPairVector> ((yyvsp[(1) - (2)].replType), *(yyvsp[(2) - (2)].transducerPairVector));
         delete (yyvsp[(2) - (2)].transducerPairVector);
         }
    break;

  case 35:

/* Line 1806 of yacc.c  */
#line 542 "xre_parse.yy"
    {
            HfstTransducerPairVector * ContextVector = new HfstTransducerPairVector();
            ContextVector->push_back(*(yyvsp[(1) - (1)].transducerPair));
            (yyval.transducerPairVector) = ContextVector;
            delete (yyvsp[(1) - (1)].transducerPair);
         }
    break;

  case 36:

/* Line 1806 of yacc.c  */
#line 550 "xre_parse.yy"
    {
            (yyvsp[(1) - (3)].transducerPairVector)->push_back(*(yyvsp[(3) - (3)].transducerPair));
            (yyval.transducerPairVector) = (yyvsp[(1) - (3)].transducerPairVector);
            delete (yyvsp[(3) - (3)].transducerPair);
         }
    break;

  case 37:

/* Line 1806 of yacc.c  */
#line 558 "xre_parse.yy"
    {
            if (hfst::xre::has_non_identity_pairs((yyvsp[(1) - (3)].transducer))) // if non-identity symbols present..
            {
              xreerror("Contexts need to be automata");
              YYABORT;
            }
            if (hfst::xre::has_non_identity_pairs((yyvsp[(3) - (3)].transducer))) // if non-identity symbols present..
            {
              xreerror("Contexts need to be automata");
              YYABORT;
            }
            
            HfstTransducer t1(*(yyvsp[(1) - (3)].transducer));
            HfstTransducer t2(*(yyvsp[(3) - (3)].transducer));

             if (hfst::xre::is_weighted())
             {
               hfst::xre::has_weight_been_zeroed=false;
               t1.transform_weights(&hfst::xre::zero_weights);
             }
             t1.optimize().prune_alphabet(false);

             if (hfst::xre::is_weighted())
             {
               t2.transform_weights(&hfst::xre::zero_weights);
               hfst::xre::has_weight_been_zeroed=false;
             }
             t2.optimize().prune_alphabet(false);

            (yyval.transducerPair) = new HfstTransducerPair(t1, t2);
            delete (yyvsp[(1) - (3)].transducer); delete (yyvsp[(3) - (3)].transducer);
         }
    break;

  case 38:

/* Line 1806 of yacc.c  */
#line 591 "xre_parse.yy"
    {
            if (hfst::xre::has_non_identity_pairs((yyvsp[(1) - (2)].transducer))) // if non-identity symbols present..
            {
              xreerror("Contexts need to be automata");
              YYABORT;
            }

            HfstTransducer t1(*(yyvsp[(1) - (2)].transducer));
            
            if (hfst::xre::is_weighted())
            {
              hfst::xre::has_weight_been_zeroed=false;
              t1.transform_weights(&hfst::xre::zero_weights);
              hfst::xre::has_weight_been_zeroed=false;
            }
            t1.optimize().prune_alphabet(false);

            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(t1, epsilon);
            delete (yyvsp[(1) - (2)].transducer);
         }
    break;

  case 39:

/* Line 1806 of yacc.c  */
#line 613 "xre_parse.yy"
    {

            if (hfst::xre::has_non_identity_pairs((yyvsp[(2) - (2)].transducer))) // if non-identity symbols present..
            {
              xreerror("Contexts need to be automata");
              YYABORT;
            }
            
            HfstTransducer t1(*(yyvsp[(2) - (2)].transducer));

            if (hfst::xre::is_weighted())
            {
              hfst::xre::has_weight_been_zeroed=false;
              t1.transform_weights(&hfst::xre::zero_weights);
              hfst::xre::has_weight_been_zeroed=false;
            }
            t1.optimize().prune_alphabet(false);
             
            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(epsilon, t1);
            delete (yyvsp[(2) - (2)].transducer);
         }
    break;

  case 40:

/* Line 1806 of yacc.c  */
#line 636 "xre_parse.yy"
    {
            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(epsilon, epsilon);
          }
    break;

  case 41:

/* Line 1806 of yacc.c  */
#line 642 "xre_parse.yy"
    {
            (yyval.replType) = REPL_UP;
         }
    break;

  case 42:

/* Line 1806 of yacc.c  */
#line 646 "xre_parse.yy"
    {
            (yyval.replType) = REPL_RIGHT;
         }
    break;

  case 43:

/* Line 1806 of yacc.c  */
#line 650 "xre_parse.yy"
    {
            (yyval.replType) = REPL_LEFT;
         }
    break;

  case 44:

/* Line 1806 of yacc.c  */
#line 654 "xre_parse.yy"
    {
            (yyval.replType) = REPL_DOWN;
         }
    break;

  case 45:

/* Line 1806 of yacc.c  */
#line 660 "xre_parse.yy"
    {
            (yyval.replaceArrow) = E_REPLACE_RIGHT;
         }
    break;

  case 46:

/* Line 1806 of yacc.c  */
#line 664 "xre_parse.yy"
    {
            (yyval.replaceArrow) = E_OPTIONAL_REPLACE_RIGHT;
         }
    break;

  case 47:

/* Line 1806 of yacc.c  */
#line 668 "xre_parse.yy"
    {
            (yyval.replaceArrow) = E_RTL_LONGEST_MATCH;
         }
    break;

  case 48:

/* Line 1806 of yacc.c  */
#line 672 "xre_parse.yy"
    {
            (yyval.replaceArrow) = E_RTL_SHORTEST_MATCH;
         }
    break;

  case 49:

/* Line 1806 of yacc.c  */
#line 676 "xre_parse.yy"
    {
            (yyval.replaceArrow) = E_LTR_LONGEST_MATCH;
         }
    break;

  case 50:

/* Line 1806 of yacc.c  */
#line 680 "xre_parse.yy"
    {
            (yyval.replaceArrow) = E_LTR_SHORTEST_MATCH;
         }
    break;

  case 51:

/* Line 1806 of yacc.c  */
#line 684 "xre_parse.yy"
    {
        	 (yyval.replaceArrow) =  E_REPLACE_LEFT;
         }
    break;

  case 52:

/* Line 1806 of yacc.c  */
#line 688 "xre_parse.yy"
    {
        	 (yyval.replaceArrow) = E_OPTIONAL_REPLACE_LEFT;
         }
    break;

  case 53:

/* Line 1806 of yacc.c  */
#line 694 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 54:

/* Line 1806 of yacc.c  */
#line 695 "xre_parse.yy"
    {
            xreerror("No shuffle");
            //$$ = $1;
            delete (yyvsp[(3) - (3)].transducer);
            YYABORT;
        }
    break;

  case 55:

/* Line 1806 of yacc.c  */
#line 701 "xre_parse.yy"
    {
            (yyval.transducer) = new HfstTransducer( before (*(yyvsp[(1) - (3)].transducer), *(yyvsp[(3) - (3)].transducer)) );
            delete (yyvsp[(1) - (3)].transducer); delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 56:

/* Line 1806 of yacc.c  */
#line 705 "xre_parse.yy"
    {
            (yyval.transducer) = new HfstTransducer( after (*(yyvsp[(1) - (3)].transducer), *(yyvsp[(3) - (3)].transducer)) );
            delete (yyvsp[(1) - (3)].transducer); delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 57:

/* Line 1806 of yacc.c  */
#line 712 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 58:

/* Line 1806 of yacc.c  */
#line 714 "xre_parse.yy"
    {
            (yyval.transducer) = new HfstTransducer( restriction(*(yyvsp[(1) - (3)].transducer), *(yyvsp[(3) - (3)].transducerPairVector)) ) ;
            delete (yyvsp[(1) - (3)].transducer);
            delete (yyvsp[(3) - (3)].transducerPairVector);
        }
    break;

  case 59:

/* Line 1806 of yacc.c  */
#line 720 "xre_parse.yy"
    {
            xreerror("No Arrows");
            //$$ = $1;
            delete (yyvsp[(3) - (5)].transducer);
            delete (yyvsp[(5) - (5)].transducer);
            YYABORT;
        }
    break;

  case 60:

/* Line 1806 of yacc.c  */
#line 728 "xre_parse.yy"
    {
            xreerror("No Arrows");
            //$$ = $1;
            delete (yyvsp[(3) - (5)].transducer);
            delete (yyvsp[(5) - (5)].transducer);
            YYABORT;
        }
    break;

  case 61:

/* Line 1806 of yacc.c  */
#line 738 "xre_parse.yy"
    {
            HfstTransducerPairVector * ContextVector = new HfstTransducerPairVector();
            ContextVector->push_back(*(yyvsp[(1) - (1)].transducerPair));
            (yyval.transducerPairVector) = ContextVector;
            delete (yyvsp[(1) - (1)].transducerPair);
         }
    break;

  case 62:

/* Line 1806 of yacc.c  */
#line 746 "xre_parse.yy"
    {
            (yyvsp[(1) - (3)].transducerPairVector)->push_back(*(yyvsp[(3) - (3)].transducerPair));
            (yyval.transducerPairVector) = (yyvsp[(1) - (3)].transducerPairVector);
            delete (yyvsp[(3) - (3)].transducerPair);
         }
    break;

  case 63:

/* Line 1806 of yacc.c  */
#line 755 "xre_parse.yy"
    {
            (yyval.transducerPair) = new HfstTransducerPair(*(yyvsp[(1) - (3)].transducer), *(yyvsp[(3) - (3)].transducer));
            delete (yyvsp[(1) - (3)].transducer); delete (yyvsp[(3) - (3)].transducer);
         }
    break;

  case 64:

/* Line 1806 of yacc.c  */
#line 760 "xre_parse.yy"
    {
           // std::cerr << "Mapping: \n" << *$1  << std::endl;
            
            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            
           // std::cerr << "Epsilon: \n" << epsilon  << std::endl;
            (yyval.transducerPair) = new HfstTransducerPair(*(yyvsp[(1) - (2)].transducer), epsilon);
            delete (yyvsp[(1) - (2)].transducer);
         }
    break;

  case 65:

/* Line 1806 of yacc.c  */
#line 770 "xre_parse.yy"
    {
            HfstTransducer epsilon(hfst::internal_epsilon, hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(epsilon, *(yyvsp[(2) - (2)].transducer));
            delete (yyvsp[(2) - (2)].transducer);
         }
    break;

  case 66:

/* Line 1806 of yacc.c  */
#line 776 "xre_parse.yy"
    {
            HfstTransducer empty(hfst::xre::format);
            (yyval.transducerPair) = new HfstTransducerPair(empty, empty);
         }
    break;

  case 67:

/* Line 1806 of yacc.c  */
#line 783 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 68:

/* Line 1806 of yacc.c  */
#line 784 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->disjunct(*(yyvsp[(3) - (3)].transducer), harmonize_);
            delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 69:

/* Line 1806 of yacc.c  */
#line 788 "xre_parse.yy"
    {
        // std::cerr << "Intersection: \n"  << std::endl;
            (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->intersect(*(yyvsp[(3) - (3)].transducer), harmonize_).optimize().prune_alphabet(false);
            delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 70:

/* Line 1806 of yacc.c  */
#line 793 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->subtract(*(yyvsp[(3) - (3)].transducer), harmonize_).prune_alphabet(false);
            delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 71:

/* Line 1806 of yacc.c  */
#line 797 "xre_parse.yy"
    {
            xreerror("No upper minus");
            //$$ = $1;
            delete (yyvsp[(3) - (3)].transducer);
            YYABORT;
        }
    break;

  case 72:

/* Line 1806 of yacc.c  */
#line 803 "xre_parse.yy"
    {
            xreerror("No lower minus");
            //$$ = $1;
            delete (yyvsp[(3) - (3)].transducer);
            YYABORT;
        }
    break;

  case 73:

/* Line 1806 of yacc.c  */
#line 809 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->priority_union(*(yyvsp[(3) - (3)].transducer));
            delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 74:

/* Line 1806 of yacc.c  */
#line 813 "xre_parse.yy"
    {
            HfstTransducer* left = new HfstTransducer(*(yyvsp[(1) - (3)].transducer));
            HfstTransducer* right =  new HfstTransducer(*(yyvsp[(3) - (3)].transducer));
            right->invert();
            left->invert();
            (yyval.transducer) = & (left->priority_union(*right).invert());
            delete (yyvsp[(1) - (3)].transducer); delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 75:

/* Line 1806 of yacc.c  */
#line 823 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 76:

/* Line 1806 of yacc.c  */
#line 824 "xre_parse.yy"
    {
        (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->concatenate(*(yyvsp[(2) - (2)].transducer), harmonize_);
        delete (yyvsp[(2) - (2)].transducer);
        }
    break;

  case 77:

/* Line 1806 of yacc.c  */
#line 830 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 78:

/* Line 1806 of yacc.c  */
#line 831 "xre_parse.yy"
    {
            // this is how ignoring is done in foma and xfst
            (yyvsp[(1) - (3)].transducer)->harmonize(*(yyvsp[(3) - (3)].transducer), true /*force harmonization also for foma type*/);
            (yyval.transducer) = & (yyvsp[(1) - (3)].transducer)->insert_freely(*(yyvsp[(3) - (3)].transducer), false); // no harmonization
            delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 79:

/* Line 1806 of yacc.c  */
#line 837 "xre_parse.yy"
    {
            xreerror("No ignoring internally");
            //$$ = $1;
            delete (yyvsp[(3) - (3)].transducer);
            YYABORT;
        }
    break;

  case 80:

/* Line 1806 of yacc.c  */
#line 843 "xre_parse.yy"
    {
            xreerror("No left quotient");
            //$$ = $1;
            delete (yyvsp[(3) - (3)].transducer);
            YYABORT;
        }
    break;

  case 81:

/* Line 1806 of yacc.c  */
#line 851 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 82:

/* Line 1806 of yacc.c  */
#line 852 "xre_parse.yy"
    {
       		// TODO: forbid pair complement (ie ~a:b)
       		HfstTransducer complement = HfstTransducer::identity_pair( hfst::xre::format );
       		complement.repeat_star().optimize();
       		complement.subtract(*(yyvsp[(2) - (2)].transducer)).prune_alphabet(false);
       		(yyval.transducer) = new HfstTransducer(complement);
   			delete (yyvsp[(2) - (2)].transducer);
        }
    break;

  case 83:

/* Line 1806 of yacc.c  */
#line 860 "xre_parse.yy"
    {
            // std::cerr << "Containment: \n" << std::endl;
            if (hfst::xre::has_non_identity_pairs((yyvsp[(2) - (2)].transducer))) // if non-identity symbols present..
            {
              hfst::xre::warn("warning: using transducer that is non an automaton in containment\n");
              (yyval.transducer) = hfst::xre::contains((yyvsp[(2) - (2)].transducer)); // ..resort to simple containment
            }
            else
            {
              (yyval.transducer) = hfst::xre::contains_with_weight((yyvsp[(2) - (2)].transducer), 0);
            }
            delete (yyvsp[(2) - (2)].transducer);
        }
    break;

  case 84:

/* Line 1806 of yacc.c  */
#line 873 "xre_parse.yy"
    {
            // std::cerr << "Containment: \n" << std::endl;
            if (hfst::xre::has_non_identity_pairs((yyvsp[(3) - (3)].transducer))) // if non-identity symbols present..
            {
              xreerror("Containment with weight only works with automata");
              YYABORT;
            }
            (yyval.transducer) = hfst::xre::contains_with_weight((yyvsp[(3) - (3)].transducer), hfst::double_to_float((yyvsp[(2) - (3)].weight)));
            delete (yyvsp[(3) - (3)].transducer);
        }
    break;

  case 85:

/* Line 1806 of yacc.c  */
#line 883 "xre_parse.yy"
    {
            //std::cerr << "Contain 1 \n"<< std::endl;

            (yyval.transducer) = hfst::xre::contains_once((yyvsp[(2) - (2)].transducer));
            delete (yyvsp[(2) - (2)].transducer);
        }
    break;

  case 86:

/* Line 1806 of yacc.c  */
#line 889 "xre_parse.yy"
    {
            (yyval.transducer) = hfst::xre::contains_once_optional((yyvsp[(2) - (2)].transducer));
            delete (yyvsp[(2) - (2)].transducer);
        }
    break;

  case 87:

/* Line 1806 of yacc.c  */
#line 895 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 88:

/* Line 1806 of yacc.c  */
#line 896 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->repeat_star();
        }
    break;

  case 89:

/* Line 1806 of yacc.c  */
#line 899 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->repeat_plus();
        }
    break;

  case 90:

/* Line 1806 of yacc.c  */
#line 902 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->reverse();
        }
    break;

  case 91:

/* Line 1806 of yacc.c  */
#line 905 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->invert();
        }
    break;

  case 92:

/* Line 1806 of yacc.c  */
#line 908 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->input_project();
        }
    break;

  case 93:

/* Line 1806 of yacc.c  */
#line 911 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->output_project();
        }
    break;

  case 94:

/* Line 1806 of yacc.c  */
#line 914 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->repeat_n((yyvsp[(2) - (2)].value));
        }
    break;

  case 95:

/* Line 1806 of yacc.c  */
#line 917 "xre_parse.yy"
    {
            //std::cerr << "value is ::::: \n"<< $2 << std::endl;
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->repeat_n_plus((yyvsp[(2) - (2)].value)+1);
        }
    break;

  case 96:

/* Line 1806 of yacc.c  */
#line 921 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->repeat_n_minus((yyvsp[(2) - (2)].value)-1);
        }
    break;

  case 97:

/* Line 1806 of yacc.c  */
#line 924 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->repeat_n_to_k((yyvsp[(2) - (2)].values)[0], (yyvsp[(2) - (2)].values)[1]);
            free((yyvsp[(2) - (2)].values));
        }
    break;

  case 98:

/* Line 1806 of yacc.c  */
#line 930 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 99:

/* Line 1806 of yacc.c  */
#line 931 "xre_parse.yy"
    {
            HfstTransducer* any = new HfstTransducer(hfst::internal_identity,
                                        hfst::xre::format);
            (yyval.transducer) = & ( any->subtract(*(yyvsp[(2) - (2)].transducer)));
            delete (yyvsp[(2) - (2)].transducer);
        }
    break;

  case 100:

/* Line 1806 of yacc.c  */
#line 946 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 101:

/* Line 1806 of yacc.c  */
#line 947 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(2) - (3)].transducer)->optimize();
        }
    break;

  case 102:

/* Line 1806 of yacc.c  */
#line 951 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(2) - (7)].transducer)->cross_product(*(yyvsp[(6) - (7)].transducer));
            delete (yyvsp[(6) - (7)].transducer);
        }
    break;

  case 103:

/* Line 1806 of yacc.c  */
#line 956 "xre_parse.yy"
    {
     	    HfstTransducer * tmp = hfst::xre::xfst_curly_label_to_transducer((yyvsp[(5) - (5)].label),(yyvsp[(5) - (5)].label));
            free((yyvsp[(5) - (5)].label));
            (yyval.transducer) = & (yyvsp[(2) - (5)].transducer)->cross_product(*tmp);
            delete tmp;
        }
    break;

  case 104:

/* Line 1806 of yacc.c  */
#line 963 "xre_parse.yy"
    {
     	    HfstTransducer * tmp = hfst::xre::xfst_curly_label_to_transducer((yyvsp[(1) - (5)].label),(yyvsp[(1) - (5)].label));
            free((yyvsp[(1) - (5)].label));
            (yyval.transducer) = & (yyvsp[(4) - (5)].transducer)->cross_product(*tmp);
            delete tmp;
        }
    break;

  case 105:

/* Line 1806 of yacc.c  */
#line 970 "xre_parse.yy"
    {
            HfstTransducer * tmp = hfst::xre::expand_definition((yyvsp[(5) - (5)].label));
            free((yyvsp[(5) - (5)].label));
            (yyval.transducer) = & (yyvsp[(2) - (5)].transducer)->cross_product(*tmp);
            delete tmp;
        }
    break;

  case 106:

/* Line 1806 of yacc.c  */
#line 977 "xre_parse.yy"
    {
            (yyval.transducer) = hfst::xre::expand_definition((yyvsp[(1) - (5)].label));
            free((yyvsp[(1) - (5)].label));
            (yyval.transducer) = & (yyval.transducer)->cross_product(*(yyvsp[(4) - (5)].transducer));
            delete (yyvsp[(4) - (5)].transducer);
        }
    break;

  case 107:

/* Line 1806 of yacc.c  */
#line 983 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(2) - (4)].transducer)->set_final_weights(hfst::double_to_float((yyvsp[(4) - (4)].weight)), true).optimize();
        }
    break;

  case 108:

/* Line 1806 of yacc.c  */
#line 986 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(2) - (3)].transducer)->optionalize();
        }
    break;

  case 109:

/* Line 1806 of yacc.c  */
#line 992 "xre_parse.yy"
    {
            if (strcmp((yyvsp[(1) - (1)].label), hfst::internal_unknown.c_str()) == 0)
              {
                (yyval.transducer) = new HfstTransducer(hfst::internal_identity, hfst::xre::format);
              }
            else
              {
                (yyval.transducer) = new HfstTransducer((yyvsp[(1) - (1)].label), (yyvsp[(1) - (1)].label), hfst::xre::format);
              }
            free((yyvsp[(1) - (1)].label));
        }
    break;

  case 110:

/* Line 1806 of yacc.c  */
#line 1003 "xre_parse.yy"
    {
            HfstTransducer * tmp ;
            if (strcmp((yyvsp[(2) - (2)].label), hfst::internal_unknown.c_str()) == 0)
              {
                 tmp = new HfstTransducer(hfst::internal_identity, hfst::xre::format);
              }
            else
              {
                 tmp = new HfstTransducer((yyvsp[(2) - (2)].label), (yyvsp[(2) - (2)].label), hfst::xre::format);
              }

            (yyvsp[(1) - (2)].transducer)->disjunct(*tmp, false); // do not harmonize
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->optimize();
            free((yyvsp[(2) - (2)].label));
            delete tmp;
            }
    break;

  case 111:

/* Line 1806 of yacc.c  */
#line 1021 "xre_parse.yy"
    { (yyval.transducer) = (yyvsp[(1) - (1)].transducer); }
    break;

  case 112:

/* Line 1806 of yacc.c  */
#line 1022 "xre_parse.yy"
    {
            (yyval.transducer) = & (yyvsp[(1) - (2)].transducer)->set_final_weights(hfst::double_to_float((yyvsp[(2) - (2)].weight)), true);
        }
    break;

  case 113:

/* Line 1806 of yacc.c  */
#line 1025 "xre_parse.yy"
    {
            try {
              hfst::HfstInputStream instream((yyvsp[(1) - (1)].label));
              (yyval.transducer) = new HfstTransducer(instream);
              instream.close();
              free((yyvsp[(1) - (1)].label));
            }
            catch (const HfstException & e) {
              (void) e; // todo handle the exception
              char msg [256];
              sprintf(msg, "Error reading transducer file '%s'.", (yyvsp[(1) - (1)].label));
              xreerror(msg);
              free((yyvsp[(1) - (1)].label));
              YYABORT;
            }
        }
    break;

  case 114:

/* Line 1806 of yacc.c  */
#line 1041 "xre_parse.yy"
    {
            FILE * f = NULL;
            f = hfst::hfst_fopen((yyvsp[(1) - (1)].label), "r");
            free((yyvsp[(1) - (1)].label));
            if (f == NULL) {
              xreerror("File cannot be opened.\n");
              YYABORT;
            }
            else {
              HfstBasicTransducer tmp;
              HfstTokenizer tok;
              char line [1000];

              while( fgets(line, 1000, f) != NULL )
              {
                hfst::xre::strip_newline(line);
                StringPairVector spv = tok.tokenize(line);
                tmp.disjunct(spv, 0);
              }
              fclose(f);
              HfstTransducer * retval = new HfstTransducer(tmp, hfst::xre::format);
              retval->optimize();
              (yyval.transducer) = retval;
            }
        }
    break;

  case 115:

/* Line 1806 of yacc.c  */
#line 1066 "xre_parse.yy"
    {
            FILE * f = NULL;
            f = hfst::hfst_fopen((yyvsp[(1) - (1)].label), "r");
            free((yyvsp[(1) - (1)].label));
            if (f == NULL) {
              xreerror("File cannot be opened.\n");
              YYABORT;
            }
            else {
              HfstTokenizer tok;
              HfstBasicTransducer tmp;
              char line [1000];

              while( fgets(line, 1000, f) != NULL )
              {
                hfst::xre::strip_newline(line);
                StringPairVector spv = HfstTokenizer::tokenize_space_separated(line);
                tmp.disjunct(spv, 0);
              }
              fclose(f);
              HfstTransducer * retval = new HfstTransducer(tmp, hfst::xre::format);
              retval->optimize();
              (yyval.transducer) = retval;
            }
        }
    break;

  case 116:

/* Line 1806 of yacc.c  */
#line 1091 "xre_parse.yy"
    {
            FILE * f = NULL;
            f = hfst::hfst_fopen((yyvsp[(1) - (1)].label), "r");
            free((yyvsp[(1) - (1)].label));
            if (f == NULL) {
              xreerror("File cannot be opened.\n");
              YYABORT;
            }
            else {
              try {
                unsigned int linecount = 0;
                HfstBasicTransducer tmp = HfstBasicTransducer::read_in_prolog_format(f, linecount);
                fclose(f);
                HfstTransducer * retval = new HfstTransducer(tmp, hfst::xre::format);
                retval->optimize();
                (yyval.transducer) = retval;
              }
              catch (const HfstException & e) {
                (void) e; // todo handle the exception
                fclose(f);
                xreerror("Error reading prolog file.\n");
                YYABORT;
              }
            }
        }
    break;

  case 117:

/* Line 1806 of yacc.c  */
#line 1116 "xre_parse.yy"
    {
            FILE * f = NULL;
            f = hfst::hfst_fopen((yyvsp[(1) - (1)].label), "r");
            if (f == NULL) {
              xreerror("File cannot be opened.\n");
              fclose(f);
              free((yyvsp[(1) - (1)].label));
              YYABORT;
            }
            else {
              fclose(f);
              // read the regex in a string
              std::ifstream ifs((yyvsp[(1) - (1)].label));
              free((yyvsp[(1) - (1)].label));
              std::stringstream buffer;
              buffer << ifs.rdbuf();
              char * regex_string = strdup(buffer.str().c_str());

              // create a new scanner for evaluating the regex
              yyscan_t scanner;
              xrelex_init(&scanner);
              YY_BUFFER_STATE bs = xre_scan_string(regex_string, scanner);

              unsigned int chars_read = hfst::xre::cr;
              hfst::xre::cr = 0;

              int parse_retval = xreparse(scanner);

              xre_delete_buffer(bs,scanner);
              xrelex_destroy(scanner);

              free(regex_string);

              hfst::xre::cr = chars_read;

              (yyval.transducer) = hfst::xre::last_compiled;

              if (parse_retval != 0)
              {
                xreerror("Error parsing regex.\n");
                YYABORT;
              }
            }
        }
    break;

  case 118:

/* Line 1806 of yacc.c  */
#line 1162 "xre_parse.yy"
    {
        if (strcmp((yyvsp[(1) - (1)].label), hfst::internal_unknown.c_str()) == 0)
          {
            (yyval.transducer) = new HfstTransducer(hfst::internal_identity, hfst::xre::format);
          }
        else
          {
            // HfstTransducer * tmp = new HfstTransducer($1, hfst::xre::format);
	    // $$ = hfst::xre::expand_definition(tmp, $1);
            (yyval.transducer) = hfst::xre::expand_definition((yyvsp[(1) - (1)].label));
          }
        free((yyvsp[(1) - (1)].label));
     }
    break;

  case 119:

/* Line 1806 of yacc.c  */
#line 1176 "xre_parse.yy"
    {
     	(yyval.transducer) = hfst::xre::xfst_label_to_transducer((yyvsp[(1) - (3)].label),(yyvsp[(3) - (3)].label));
        free((yyvsp[(1) - (3)].label));
        free((yyvsp[(3) - (3)].label));
     }
    break;

  case 120:

/* Line 1806 of yacc.c  */
#line 1181 "xre_parse.yy"
    {
        (yyval.transducer) = hfst::xre::xfst_label_to_transducer((yyvsp[(1) - (3)].label),(yyvsp[(1) - (3)].label));
        free((yyvsp[(1) - (3)].label));
        HfstTransducer * tmp = hfst::xre::xfst_curly_label_to_transducer((yyvsp[(3) - (3)].label),(yyvsp[(3) - (3)].label));
        free((yyvsp[(3) - (3)].label));
        (yyval.transducer) = & (yyval.transducer)->cross_product(*tmp);
        delete tmp;
     }
    break;

  case 121:

/* Line 1806 of yacc.c  */
#line 1189 "xre_parse.yy"
    {
        HfstTransducer * tmp = hfst::xre::xfst_label_to_transducer((yyvsp[(3) - (3)].label),(yyvsp[(3) - (3)].label));
        free((yyvsp[(3) - (3)].label));
        (yyval.transducer) = hfst::xre::xfst_curly_label_to_transducer((yyvsp[(1) - (3)].label),(yyvsp[(1) - (3)].label));
        free((yyvsp[(1) - (3)].label));
        (yyval.transducer) = & (yyval.transducer)->cross_product(*tmp);
        delete tmp;
     }
    break;

  case 122:

/* Line 1806 of yacc.c  */
#line 1197 "xre_parse.yy"
    {
     	(yyval.transducer) = hfst::xre::xfst_curly_label_to_transducer((yyvsp[(1) - (1)].label),(yyvsp[(1) - (1)].label));
        free((yyvsp[(1) - (1)].label));
     }
    break;

  case 123:

/* Line 1806 of yacc.c  */
#line 1201 "xre_parse.yy"
    {
     	(yyval.transducer) = hfst::xre::xfst_curly_label_to_transducer((yyvsp[(1) - (3)].label),(yyvsp[(3) - (3)].label));
        free((yyvsp[(1) - (3)].label));
	free((yyvsp[(3) - (3)].label));
     }
    break;

  case 124:

/* Line 1806 of yacc.c  */
#line 1207 "xre_parse.yy"
    {
            if (! hfst::xre::is_valid_function_call((yyvsp[(1) - (3)].label), (yyvsp[(2) - (3)].transducerVector))) {
              delete (yyvsp[(1) - (3)].label); delete (yyvsp[(2) - (3)].transducerVector);
              return EXIT_FAILURE;
            }
            else {
              // create a new scanner for evaluating the function
              yyscan_t scanner;
              xrelex_init(&scanner);
              YY_BUFFER_STATE bs = xre_scan_string(hfst::xre::get_function_xre((yyvsp[(1) - (3)].label)),scanner);

              // define special variables so that function arguments get the values given in regexp list
              if (! hfst::xre::define_function_args((yyvsp[(1) - (3)].label), (yyvsp[(2) - (3)].transducerVector)))
              {
                xreerror("Could not define function args.\n");  // TODO: more informative message
                delete (yyvsp[(1) - (3)].label); delete (yyvsp[(2) - (3)].transducerVector);
                YYABORT;
              }

              delete (yyvsp[(2) - (3)].transducerVector);
              // if we are scanning a function definition for argument symbols,
              // do not include the characters read when evaluating functions inside it
              unsigned int chars_read = hfst::xre::cr;

              int parse_retval = xreparse(scanner);

              hfst::xre::cr = chars_read;
              hfst::xre::undefine_function_args((yyvsp[(1) - (3)].label));
              delete (yyvsp[(1) - (3)].label);

              xre_delete_buffer(bs,scanner);
              xrelex_destroy(scanner);

              (yyval.transducer) = hfst::xre::last_compiled;

              if (parse_retval != 0)
              {
                YYABORT;
              }
            }
        }
    break;

  case 126:

/* Line 1806 of yacc.c  */
#line 1258 "xre_parse.yy"
    {
       hfst::xre::check_multichar_symbol((yyvsp[(1) - (1)].label));
       (yyval.label) = (yyvsp[(1) - (1)].label);
     }
    break;

  case 127:

/* Line 1806 of yacc.c  */
#line 1262 "xre_parse.yy"
    {
       hfst::xre::check_multichar_symbol((yyvsp[(1) - (1)].label));
       (yyval.label) = (yyvsp[(1) - (1)].label);
     }
    break;

  case 129:

/* Line 1806 of yacc.c  */
#line 1270 "xre_parse.yy"
    {
       // Symbols of form <foo> are not harmonized in xfst, that is why
       // they need to be escaped as @_<foo>_@.
       // $$ = hfst::xre::escape_enclosing_angle_brackets($1);
       hfst::xre::warn_about_hfst_special_symbol((yyvsp[(1) - (1)].label));
       hfst::xre::warn_about_xfst_special_symbol((yyvsp[(1) - (1)].label));
       (yyval.label) = (yyvsp[(1) - (1)].label);
     }
    break;

  case 130:

/* Line 1806 of yacc.c  */
#line 1278 "xre_parse.yy"
    {
        (yyval.label) = strdup(hfst::internal_epsilon.c_str());
     }
    break;

  case 131:

/* Line 1806 of yacc.c  */
#line 1281 "xre_parse.yy"
    {
        (yyval.label) = strdup(hfst::internal_unknown.c_str());
     }
    break;

  case 132:

/* Line 1806 of yacc.c  */
#line 1284 "xre_parse.yy"
    {
        (yyval.label) = strdup("@#@");
     }
    break;

  case 133:

/* Line 1806 of yacc.c  */
#line 1289 "xre_parse.yy"
    {
       (yyval.transducerVector)->push_back(*((yyvsp[(3) - (3)].transducer)));
       delete (yyvsp[(3) - (3)].transducer);
     }
    break;

  case 134:

/* Line 1806 of yacc.c  */
#line 1293 "xre_parse.yy"
    {
       (yyval.transducerVector) = new hfst::HfstTransducerVector();
       (yyval.transducerVector)->push_back(*((yyvsp[(1) - (1)].transducer)));
       delete (yyvsp[(1) - (1)].transducer);
     }
    break;

  case 135:

/* Line 1806 of yacc.c  */
#line 1300 "xre_parse.yy"
    {
        (yyval.label) = strdup((yyvsp[(1) - (1)].label));
    }
    break;



/* Line 1806 of yacc.c  */
#line 3716 "xre_parse.cc"
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
      yyerror (scanner, YY_("syntax error"));
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
        yyerror (scanner, yymsgp);
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
		      yytoken, &yylval, scanner);
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
		  yystos[yystate], yyvsp, scanner);
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
  yyerror (scanner, YY_("memory exhausted"));
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
                  yytoken, &yylval, scanner);
    }
  /* Do not reclaim the symbols of the rule which action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
		  yystos[*yyssp], yyvsp, scanner);
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
#line 1304 "xre_parse.yy"



