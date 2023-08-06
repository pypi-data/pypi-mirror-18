/* A Bison parser, made by GNU Bison 2.5.  */

/* Bison interface for Yacc-like parsers in C
   
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

/* Line 2068 of yacc.c  */
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
     


/* Line 2068 of yacc.c  */
#line 320 "pmatch_parse.hh"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE pmatchlval;


