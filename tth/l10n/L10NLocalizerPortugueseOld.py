#coding: latin-1
data = u'''
LSC_LOADING Carregando...

CTP_MAK FAZER UM TOON
CTP_CHOOSETEXT ESCOLHA UM TOON PARA JOGAR
CTP_PLAYTHIS Jogar com este Toon
CTP_EXIT SAIR
CTP_DELETEDIAG Voc� tem certeza que quer deletar %s? Toons deletados N�O podem ser recuperados! Se voc� realmente quer deletar este toon, digite sua senha aqui e clique em OK.
CTP_DELETE_ST_FAILED A senha est� errada!

TPS_TIPTITLE DICA TOON
TPS_GOINGTO Indo para

AREA_PLAYGROUND P�tio #generic
AREA_Toontorial Toon-torial
AREA_MAT Criar-Um-Toon
AREA_TTC Centro de Toontown
AREA_51	Area 51
AREA_SPEEDWAY Aut�dromo
AREA_DDK Porto do Donut
AREA_BRG O Brrrgh
AREA_MML Melodil�ndia
AREA_GAR Jardim
AREA_DDL Sonhol�ndia
AREA_HQ_SELL Quartel dos R�bos-vendedores
AREA_HQ_SELL_FACTORYEXT F�brica dos R�bos-vendedores
AREA_HQ_CASH Quartel dos R�bos-mercen�rios
AREA_HQ_LAW Quartel dos R�bos-da-lei
AREA_HQ_LAW_DAEXT Escrit�rio do Promotor P�blico
AREA_ACRES Bosque das Bolotas
AREA_MINIGOLF Mini Golf
AREA_HQ_BOSS Quartel General dos R�bos-chefes

MAT_TITLE T�tulo
MAT_FIRST �ltimo
MAT_LAST Primeiro

MAT_PLEASE_TYPE_A_NAME Please type your name:
MAT_TYPE_A_NAME Type-A-Name

#streets

AREA_ST_1100 Barnacle Boulevard
AREA_ST_1200 Seaweed Street
AREA_ST_1300 Lighthouse Lane

AREA_ST_2100 Silly Street
AREA_ST_2200 Loopy Lane
AREA_ST_2300 Punchline Place

AREA_ST_3100 Walrus Way
AREA_ST_3200 Sleet Street
AREA_ST_3300 Polar Place

AREA_ST_4100 Alto Avenue
AREA_ST_4200 Baritone Boulevard
AREA_ST_4300 Tenor Terrace

AREA_ST_5100 Elm Street
AREA_ST_5200 Maple Street
AREA_ST_5300 Oak Street

AREA_ST_9100 Lullaby Lane
AREA_ST_9200 Pajama Place

#end streets

#minigames

AREA_MG_TT Trolley Tracks
AREA_MG_LAB Maze Game
AREA_MG_CAN Cannon Game
AREA_MG_CAT Catching Game
AREA_MG_MM Match Minnie
AREA_MG_RIN Ring Game
AREA_MG_RG Race Game
AREA_MG_TRE Treasure Dive
AREA_MG_ESC Toon Escape
AREA_MG_VIN Jungle Vines
AREA_MG_SLN Toon Slingshot
AREA_MG_THE Cog Theif
AREA_MG_PF Photo Fun
AREA_MG_MEM Toon Memory Game
AREA_MG_TAG Toon Tag
AREA_MG_TUG Tug Of War

#end minigames

ELEVATOR_HOPOFF Descer #also for trolley

GOLF_HARD (o nome vai aqui) Dif�cil - 9 Buracos
GOLF_MED (o nome vai aqui) M�dio - 6 Buracos
GOLF_EASY (o nome vai aqui) F�cil - 3 Buracos

COGHQ_FRONT3 Tr�s da frente
COGHQ_MIDDLE6 Seis do meio
COGHQ_BACK9 Nove dos fundos

PROP_TROLLEY Jogos do Bondinho
PROP_CLOTHSTORE Loja de Roupas
PROP_PETSHOP Loja de Animais
PROP_BANK Banco
PROP_SCHOOLHOUSE Casa da Escola
PROP_HALL Prefeitura

CAT_GIRL Menina
CAT_BOY Menino
CAT_CHOOSE ESCOLHA
CAT_SHUFFLE Misturar

CAT_TITLE_GENDER SEU G�NERO
CAT_TITLE_SPECIES SEU TIPO
CAT_TITLE_COLOR SUA COR
CAT_TITLE_CLOTHES SUAS ROUPAS
CAT_TITLE_NAME SEU NOME

CAT_HEAD Cabe�a
CAT_TORSO Corpo
CAT_LEGS Pernas
CAT_SHIRT Camisa
CAT_SHORTS Bermuda
CAT_SKIRT Saia

SPC_CAT Gato
SPC_PIG Porco
SPC_DOG Cachorro
SPC_HORSE Cavalo
SPC_BEAR Urso
SPC_MOUSE Rato
SPC_DUCK Pato
SPC_RABBIT Coelho
SPC_MONKEY Macaco

ACCESSORY_HAT Hat
ACCESSORY_GLASSES Glasses
ACCESSORY_BACKPACK Backpack
ACCESSORY_SHOES Shoes

CAT_ACCESSORIES Accessories
CAT_CLOTHES Clothes

COLOR_GOLDEN Dourado
COLOR_LIGHTBLUE Azul Claro
COLOR_DARKBLUE Azul Escuro
COLOR_PINK Rosa
COLOR_DARKGREEN Verde Escuro
COLOR_LIGHTGREEN Verde Claro
COLOR_BROWN Marrom
COLOR_PURPLE Roxo
COLOR_RED Vermelho
COLOR_ORANGE Laranja
COLOR_YELLOW Amarelo

APFriends Amigos
APWhisper Whisper #forgot this lol
APSecrets Amigos Secretos
APGoTo Ir para
APPet Rabisco
APIgnore Ignorar
APReport Reportar
APDetail Detalhes
APGroupInvite Convidar
APGroupMember J� est� no grupo
APGroupMemberKick Remover

FLPNewFriend Novo Amigo
FLPSecrets Amigos Secretos
FLPOnlineFriends AMIGOS\\nONLINE
FLPAllFriends TODOS\\nAMIGOS
FLPIgnoredFriends TOONS\\nIGNORADOS
FLPPets RABISCOS\\nPR�XIMOS
FLPPlayers ALL PLAYER\\nFRIENDS #unused
FLPOnlinePlayers ONLINE PLAYER\\nFRIENDS #unused

BOOK_OPT_OptionsPageTitle Op��es
BOOK_OPT_OptionsTabTitle Op��es{0}& C�digos
BOOK_OPT_OptionsPagePurchase Subscribe #not used lol
BOOK_OPT_OptionsPageLogout Sair
BOOK_OPT_OptionsPageExitToontown Sair de Toontown
BOOK_OPT_OptionsPageMusicOnLabel M�sica est� ligada.
BOOK_OPT_OptionsPageMusicOffLabel M�sica est� desligada.
BOOK_OPT_OptionsPageSFXOnLabel Efeitos est�o ligados.
BOOK_OPT_OptionsPageSFXOffLabel Efeitos est�o desligados.
BOOK_OPT_OptionsPageToonChatSoundsOnLabel    Efeitos de chat est�o ligados.
BOOK_OPT_OptionsPageToonChatSoundsOffLabel    Efeitos de chat est�o ligados.
BOOK_OPT_OptionsPageFriendsEnabledLabel Aceitando pedidos de amizade.
BOOK_OPT_OptionsPageFriendsDisabledLabel N�o aceitando pedidos de amizade.
BOOK_OPT_OptionsPageWhisperEnabledLabel Permitindo sussurros de qualquer um.
BOOK_OPT_OptionsPageWhisperDisabledLabel Permitindo sussurros apenas de amigos.
BOOK_OPT_OptionsPageSpeedChatStyleLabel Cor do Chat R�pido
BOOK_OPT_OptionsPageDisplayWindowed Janela
BOOK_OPT_OptionsPageDisplayEmbedded No navegador
BOOK_OPT_OptionsPageSelect Selecionar
BOOK_OPT_OptionsPageToggleOn Ligar
BOOK_OPT_OptionsPageToggleOff Desligar
BOOK_OPT_OptionsPageChange Mudar
BOOK_OPT_OptionsPageDisplaySettings Display: %(screensize)s, %(api)s
BOOK_OPT_OptionsPageDisplaySettingsNoApi Display: %(screensize)s
BOOK_OPT_OptionsPageExitConfirm Sair de Toontown?
BOOK_OPT_OptionsPageCodesTab Digitar C�digo
BOOK_OPT_CdrPageTitle Digite um C�digo
BOOK_OPT_CdrInstructions Digita seu c�digo pra receber um item especial na caixa de correio.
BOOK_OPT_CdrResultSuccess Parab�ns! Verifique sua caixa de correio pra receber seu item!
BOOK_OPT_CdrResultInvalidCode C�digo invalido. Tente novamente.
BOOK_OPT_CdrResultExpiredCode Sinto muito, este c�digo expirou.
BOOK_OPT_CdrResultUnknownError Sinto muito, este c�digo n�o pode ser aplicado ao seu Toon.
BOOK_OPT_CdrResultMailboxFull Sua caixa de correio est� cheia. Remova um item e tente novamente.
BOOK_OPT_CdrResultAlreadyInMailbox Voc� j� recebeu este item. Verifique sua caixa de correio.
BOOK_OPT_CdrResultAlreadyInQueue Seu item est� a caminho. Verifique sua caixa de correio em alguns minutos.
BOOK_OPT_CdrResultAlreadyInCloset Voc� j� recebeu esse item. Verifique seu closet.
BOOK_OPT_CdrResultAlreadyBeingWorn Voc� j� recebeu esse item, e est� usando-o!
BOOK_OPT_CdrResultAlreadyReceived Voc� j� recebeu esse item.
BOOK_OPT_CdrResultTooManyFails Sinto muito, voc� errou muitas vezes. Tente novamente mais tarde.
BOOK_OPT_CdrResultServiceUnavailable Sinto muito, este recurso est� temporariamente desativado. Tente novamente mais tarde.
BOOK_OPT_NameShopSubmitButton Enviar
BOOK_DIST Distritos
BOOK_DIST_ABOUT Cada distrito � uma c�pia do mundo de Toontown House. Para ir a um novo distrito, clique em seu nome.
BOOK_MAP Mapa
BOOK_MAP_BACKTOSZ Voltar ao P�tio
BOOK_MAP_BACKTOHQ Voltar ao Quartel Cog
BOOK_MAP_HOME Ir para casa
BOOK_MAP_UR Voc� est� em:
BOOK_MAP_ESTATE Voc� est�{0}na sua casa
BOOK_MAP_SOMEONES Voc� est� na casa %s
BOOK_MAP_GOTO Ir Para
BOOK_DISGUISE_PARTS Perna Esquerda Superior,Perna Esquerda Inferior,P� Esquerdo,Perna Direita Superior,Perna Direita Inferior,P� Direito,Ombro Esquerdo,Ombro Direito,Peito,Medidor de sa�de,Pelvis,Bra�o Esquerdo Superior,Bra�o Esquerdo Inferior,M�o Esquerda,Bra�o Direito Superior,Bra�o Direito Inferior,M�o Direita
BOOK_DISGUISE_TITLE Disfar�e Cog
BOOK_DISGUISE_ALERT Pronto para{0}promo��o!
BOOK_DISGUISE_LEVEL N�vel %s
BOOK_DISGUISE_FULL Cheio
BOOK_SUIT_TITLE Galeria de Cogs
BOOK_SUIT_MYSTERY ???
BOOK_SUIT_QUOTA %s de %s
BOOK_SUIT_RADAR %s presente(s)
BOOK_SUIT_RADARSING %s edif�cio
BOOK_SUIT_RADARPLURAL %s edif�cios
BOOK_SUIT_ISSUE Invocar

SPEECH_TUT_COMEHERE Vem aqui! Use as teclas pra se mover!
SPEECH_TUT_GOTOTTC O resto do Toontorial t� em desenvolvimento, ent�o voc� vai direto pra o Centro de Toontown!

COG_SELLBOT Rob�-vendedor
COG_SELLBOT0 Rei da Incerta
COG_SELLBOT1 Operador de Telemarkerting
COG_SELLBOT2 Dr. Voc�-n�o-sabe-com-quem-est�-falando #yep, its long lol
COG_SELLBOT3 Amigo da on�a
COG_SELLBOT4 Agitador
COG_SELLBOT5 Duas Caras
COG_SELLBOT6 Amizade F�cil
COG_SELLBOT7 Dr. Celebridade

COG_CASHBOT Rob�-mercen�rio
COG_CASHBOT0 Farsante
COG_CASHBOT1 M�o-de-vaca
COG_CASHBOT2 P�o-duro
COG_CASHBOT3 Contador de Balinhas
COG_CASHBOT4 Destruidor de N�meros
COG_CASHBOT5 Sacos de Dinheiro
COG_CASHBOT6 Agiota
COG_CASHBOT7 Bar�o Ladr�o

COG_LAWBOT Rob�-da-lei
COG_LAWBOT0 Comensal
COG_LAWBOT1 Sanguessuga
COG_LAWBOT2 Duplo-sentido
COG_LAWBOT3 Perseguidor de Ambul�ncias
COG_LAWBOT4 Golpe Sujo
COG_LAWBOT5 Rela��es P�blicas
COG_LAWBOT6 Macaco Velho
COG_LAWBOT7 Figur�o

COG_BOSSBOT Rob�-chefe
COG_BOSSBOT0 Puxa-saco
COG_BOSSBOT1 Rato de Escrit�rio
COG_BOSSBOT2 Vaquinha de Pres�pio
COG_BOSSBOT3 Micro-empres�rio
COG_BOSSBOT4 Fac�o
COG_BOSSBOT5 Ca�a-talentos
COG_BOSSBOT6 Aventureiro Corporativo
COG_BOSSBOT7 O Rei da Cocada Preta

COG_TAG %s\\n%s\\nN�vel %s
COG_TAG_VER %s\\n%s\\nN�vel %s v%s.0
COG_SKEL Esqueletocog

GAG Piada

GAG_0 Toonar
GAG_0_1 Feather
GAG_0_2 Microphone
GAG_0_3 Lipstick
GAG_0_4 Bamboo Cane
GAG_0_5 Pixie Dust
GAG_0_6 Juggling Balls
GAG_0_7 High Dive

GAG_1 Armadilha
GAG_1_1 Banana Peel
GAG_1_2 Rake
GAG_1_3 Marble
GAG_1_4 Quicksand
GAG_1_5 Trapdoor
GAG_1_6 TNT
GAG_1_7 Train

GAG_2 Isca
GAG_2_1 $1 bill
GAG_2_2 Small magnet
GAG_2_3 $5 bill
GAG_2_4 Big magnet
GAG_2_5 $10 bill
GAG_2_6 Hypno Goggles
GAG_2_7 Presentation

GAG_3 Sonora
GAG_3_1 Bike Horn
GAG_3_2 Whistle
GAG_3_3 ? #forgot
GAG_3_4 Aoogah
GAG_3_5 Elephant Trunk
GAG_3_6 Fog Horn
GAG_3_7 Opera Singer

GAG_4 Lan�amento
GAG_4_1 Cupcake
GAG_4_2 ? #forgot
GAG_4_3 ? #forgot
GAG_4_4 ? #forgot
GAG_4_5 Whole Cream Pie
GAG_4_6 Birthday Cake
GAG_4_7 Wedding Cake

GAG_5 Esguicho
GAG_5_1 Flower
GAG_5_2 Cup
GAG_5_3 Squirting Gun
GAG_5_4 Sheltzer
GAG_5_5 Hose
GAG_5_6 Cloud
GAG_5_7 Geyser

GAG_6 Cadente
GAG_6_1 Flower Pot
GAG_6_2 Sandbag
GAG_6_3 Anvil
GAG_6_4 Heavy weight
GAG_6_5 Safe
GAG_6_6 Piano
GAG_6_7 Toontanic

AREA_MG_CANNON Jogo do canh�o
'''