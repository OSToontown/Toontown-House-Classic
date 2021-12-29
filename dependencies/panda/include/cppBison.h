
#ifndef YYLTYPE
typedef
  struct yyltype
    {
      int timestamp;
      int first_line;
      int first_column;
      int last_line;
      int last_column;
      char *text;
   }
  yyltype;

#define YYLTYPE yyltype
#endif

#define	REAL	258
#define	INTEGER	259
#define	CHAR_TOK	260
#define	STRING	261
#define	SIMPLE_IDENTIFIER	262
#define	IDENTIFIER	263
#define	TYPENAME_IDENTIFIER	264
#define	SCOPING	265
#define	TYPEDEFNAME	266
#define	ELLIPSIS	267
#define	OROR	268
#define	ANDAND	269
#define	EQCOMPARE	270
#define	NECOMPARE	271
#define	LECOMPARE	272
#define	GECOMPARE	273
#define	LSHIFT	274
#define	RSHIFT	275
#define	POINTSAT_STAR	276
#define	DOT_STAR	277
#define	UNARY	278
#define	UNARY_NOT	279
#define	UNARY_NEGATE	280
#define	UNARY_MINUS	281
#define	UNARY_STAR	282
#define	UNARY_REF	283
#define	POINTSAT	284
#define	SCOPE	285
#define	PLUSPLUS	286
#define	MINUSMINUS	287
#define	TIMESEQUAL	288
#define	DIVIDEEQUAL	289
#define	MODEQUAL	290
#define	PLUSEQUAL	291
#define	MINUSEQUAL	292
#define	OREQUAL	293
#define	ANDEQUAL	294
#define	XOREQUAL	295
#define	LSHIFTEQUAL	296
#define	RSHIFTEQUAL	297
#define	TOKENPASTE	298
#define	KW_BEGIN_PUBLISH	299
#define	KW_BLOCKING	300
#define	KW_BOOL	301
#define	KW_CATCH	302
#define	KW_CHAR	303
#define	KW_WCHAR_T	304
#define	KW_CLASS	305
#define	KW_CONST	306
#define	KW_DELETE	307
#define	KW_DOUBLE	308
#define	KW_DYNAMIC_CAST	309
#define	KW_ELSE	310
#define	KW_END_PUBLISH	311
#define	KW_ENUM	312
#define	KW_EXTENSION	313
#define	KW_EXTERN	314
#define	KW_EXPLICIT	315
#define	KW_PUBLISHED	316
#define	KW_FALSE	317
#define	KW_FLOAT	318
#define	KW_FRIEND	319
#define	KW_FOR	320
#define	KW_GOTO	321
#define	KW_IF	322
#define	KW_INLINE	323
#define	KW_INT	324
#define	KW_LONG	325
#define	KW_LONGLONG	326
#define	KW_MAKE_SEQ	327
#define	KW_MUTABLE	328
#define	KW_NAMESPACE	329
#define	KW_NEW	330
#define	KW_OPERATOR	331
#define	KW_PRIVATE	332
#define	KW_PROTECTED	333
#define	KW_PUBLIC	334
#define	KW_REGISTER	335
#define	KW_RETURN	336
#define	KW_SHORT	337
#define	KW_SIGNED	338
#define	KW_SIZEOF	339
#define	KW_STATIC	340
#define	KW_STATIC_CAST	341
#define	KW_STRUCT	342
#define	KW_TEMPLATE	343
#define	KW_THROW	344
#define	KW_TRUE	345
#define	KW_TRY	346
#define	KW_TYPEDEF	347
#define	KW_TYPENAME	348
#define	KW_UNION	349
#define	KW_UNSIGNED	350
#define	KW_USING	351
#define	KW_VIRTUAL	352
#define	KW_VOID	353
#define	KW_VOLATILE	354
#define	KW_WHILE	355
#define	START_CPP	356
#define	START_CONST_EXPR	357
#define	START_TYPE	358

