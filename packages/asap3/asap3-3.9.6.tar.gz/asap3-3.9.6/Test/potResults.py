from __future__ import print_function
eEMT_Cu = [0.47567842697559737, 0.068481816907074666, 0.019826085345393984, 0.01132646115287983, 0.022377983357233955, 0.0731066493923338, 0.027518258711848098, 0.025491570294618793, 0.021181615045885227, 0.46898682857281582, 0.026739141102297026, 0.026759610673799727, 0.015851264032711754, 0.061911566132015317, 0.023294829959159546, 0.0050597565944787704, 0.019907502478251349, 0.063135715115930413, 0.44650718914713483, 0.029893364975007497, 0.018342287785060751, 0.059217431916245733, 0.015420570119832444, 0.031692759653631164, 0.010263653628126423, 0.06667856818993334, 0.011897388405913922, 0.47776792048829053, 0.019757897383688938, 0.066538161289798392, 0.019835306915341633, 0.033778027079270689, 0.021243411513096166, 0.06491212592466411, 0.0099642212687784948, 0.035890144273515556, 0.44746864500896999, 0.064547718603075843, 0.0093317887362465157, 0.019062730189749022, 0.026230523763195901, 0.062809454281547161, 0.0092549122421252683, 0.034087834301670838, 0.02894245881243851, 0.47524413604665705, 0.010284302191232886, 0.033431869721394225, 0.015324970056674214, 0.057708115565848317, 0.01065180982709979, 0.022481294970960963, 0.036976212246160767, 0.053032967512484319, 0.43342787917998571, 0.030396945539262088, 0.041006652220497042, 0.060065937012044657, 0.013677394674573407, 0.02943999299280442, 0.025914834429329403, 0.046838974420826407, 0.01702118981411882, 0.48004617364989555, 0.049403406846918685, 0.042632481530961552, -0.001737155853235528, 0.025742074902115775, 0.052686168577794845, 0.051402047441278409, 0.019961713104766243, 0.024743859831583226, 0.4645650757124451, 0.033623773961506398, 0.022216997035394037, 0.01750253113803879, 0.059112117591669566, 0.029615632408639403, -0.00011778999945555313, 0.020512471792256903, 0.060781925690456706, 0.45267844668373769, 0.026357605619768965, 0.019311410614895497, 0.052413273780727465, 0.02173671282240619, 0.028484109000634028, 0.012606403915597308, 0.065265383008167976, 0.016736349867836786, 0.46889619505753188, 0.018276349315184071, 0.06625241996299458, 0.027940249502071524, 0.031716383911984281, 0.018633044044193081, 0.061698038279611733, 0.013032914540813234, 0.03462312046460525, 0.44954644829784174, 0.066696037534771158, 0.011217087635066125, 0.014438580503250975, 0.021203832389528721, 0.06585583219731328, 0.016133478747636598, 0.034259691188626373, 0.023117613496054457, 0.47694934449233584, 0.0099518752962111101, 0.03440428486020819, 0.011066951404708369, 0.062850372397457388, 0.0092551114951064939, 0.02068208444529418, 0.029376605293834679, 0.059370174881840487, 0.43303838005595674, 0.032805923373168788, 0.033105918091147934, 0.064858405597807867, 0.010614731047466908, 0.032532130130740189, 0.018713926944324388, 0.056751802736238144, 0.012812537431188264, 0.48047805927687337, 0.033599156285930576, 0.050489219327546575, 0.0094473588612284942, 0.025436951895981608, 0.036028249389529865, 0.064287343786398665, 0.018340007162720884, 0.026542912350985937]
sEMT_Cu = [0.048044966106507152, -0.048968092230662078, -0.011218530930726379, 0.0095573520504851611, 0.0045285268396262823, -0.029016333415788353, 0.0003637045714373496, 0.028551616532011014, 0.022673205467479265, -0.016946101432451108, -0.012482267922097542, 0.021922968585862443, 0.011887514545586314, -0.039877034853046479, -0.012623896571033012, 0.015964062835746282, 0.016876836319436317, -0.027412551567251236, 0.011669654852456102, 0.018171014190533824, 0.018890862618332935, -0.016844208696240478, -0.019529628431183933, 0.017442182437113693, 0.01587411508529581, -0.047845264211378469, -0.008812346125608125, 0.0091835275188754707, 0.019413949293511167, -0.023282735018519359, 0.0069009638265106156, 0.027034615786481697, 0.017566994327294624, -0.019468441027065776, -0.023427569427673534, 0.011296447625474023, 0.028861496898371964, -0.046597178116164775, -0.0073048180098904524, 0.021429113760664874, 0.020433735707309095, -0.018367388977593786, 0.0098668602211685764, 0.03169293922333543, 0.013954114418886365, -0.021927681316878712, -0.025239236710935253, 0.0053272334003888764, 0.014583872880820317, -0.047444725581028344, -0.0043827844747037839, 0.021335446551277764, 0.01997578308596077, -0.012921344258870466, 0.037041801147957527, 0.034144445976521234, 0.0079895277036618507, -0.024134231367087228, -0.025423508524382191, -0.0010358935798761577, 0.0099841692545740851, -0.041312266588206109, -0.0013995444849008928, 0.010948065208508509, 0.018736811625882817, -0.0052746328503821029, 0.013095269487282927, 0.034066778651211764, 0.0021904735526835305, -0.026387802145343291, -0.023809178072321739, -0.0078770026652807516, 0.0066327379370073221, -0.031986664444715623, -0.00068951680608229677, 0.016759104108398398, 0.015704100905582954, 0.0025580402272352663, 0.013427568939002621, 0.030901818753997522, -0.0022071936350627733, -0.018714712200202422, -0.021096515632873101, -0.013633626203626971, -0.0022287826724043695, -0.023422105886728453, 0.00045588209093322732, 0.013775776978958132, 0.012538228221335337, 0.011174856120754549, 0.052599479341271502, 0.026388674944024509, -0.0065621925916815958, -0.026004315111916178, -0.016363451420676026, -0.019318743499491212, -0.0067739865802873408, -0.014628700765816939, 0.0020596587957297779, 0.0061763358824661833, 0.0094282014621387359, 0.018156736839996687, 0.01113931625154555, 0.014263358066819182, -0.0092553280888077408, -0.021858898156033611, -0.010811644329888116, -0.024345975652799095, -0.0058394233345728901, -0.0091242102346675621, 0.0044807276735069424, 0.0054246388509011177, 0.0045852575643312628, 0.023888301957298783, 0.0097237830163198584, 0.0012902083294964101, -0.010097415829999809, -0.0066119684034409848, -0.0045327324346425739, -0.027503535573162048, -0.0087287641499985639, -0.00081682343851625699, 0.0078052163926946279, 1.7114240508567393e-05, 0.00021176797278328884, 0.027729627430503095, 0.05221654225498247, -0.0026012617620051453, -0.012669929555729511, -0.0064681111137017393, -0.00086626658165779157, -0.024708002681397428, -0.00076527643931126571, 0.0022043622890570175, 0.012750586052854493]
eEMT_Cu_Rasm = [0.52393877406683709, 0.063341405852080701, 0.01745417816510475, 0.0092826541848141098, 0.020522262607148622, 0.069836853601750182, 0.025260920789626162, 0.014295394468934575, 0.019027650083885739, 0.5154109864824834, 0.01967618157578821, 0.019401482076457199, 0.016494504422174483, 0.060683526237644614, 0.018181325413002103, -4.5159862450905308e-05, 0.021540476088802496, 0.06022381286581302, 0.49310280516244198, 0.022383555985597159, 0.020911283055337737, 0.059587925371041628, 0.010199943339197048, 0.024970414678457953, 0.011863440905025335, 0.064694913542012511, 0.0060972620495145513, 0.52407147281729305, 0.020266734603924252, 0.064319262813751443, 0.015638617360135054, 0.02790766047473392, 0.023707226795990355, 0.064916026020551243, 0.004239062429038043, 0.030112878080458483, 0.49780952939120171, 0.059803955190342872, 0.0033658659659678847, 0.013872206720278335, 0.028110413095250308, 0.059609264552704211, 0.0055427702775587839, 0.029787423056933271, 0.029575048118288816, 0.51934512305430092, 0.0022384079335520113, 0.029749385612964918, 0.016610020374947077, 0.053784715004198347, 0.0038128880464198822, 0.019165314212207907, 0.037588224732310049, 0.047441562257987346, 0.48109312187511444, 0.026808700427830345, 0.041204718833492304, 0.057772378048806861, 0.0063232009010030232, 0.027741362012549509, 0.02682766332742359, 0.042087098554020486, 0.0088692263883238809, 0.5274814534190444, 0.046722973150069791, 0.037725763021796421, -0.0047359055892162161, 0.025423209638276045, 0.051856270603232169, 0.047810405013132051, 0.012209472041981417, 0.024647595723253701, 0.51138246188143643, 0.02659732293103767, 0.014475229005249002, 0.01819503719418103, 0.057871085979156689, 0.024518973232746433, -0.0036993413119028595, 0.022016164347238298, 0.058013122203643075, 0.49881925968327012, 0.018340281249452417, 0.021284496832258082, 0.052834388297994916, 0.016617073084906231, 0.021169046145626425, 0.014024110194019279, 0.06361872655316958, 0.011053805010720286, 0.51546340263550006, 0.018786297606651292, 0.064464066145104582, 0.023545025203995262, 0.025016248774885064, 0.021269130502367339, 0.06198148856881236, 0.0076903903126783746, 0.027888808731389769, 0.4999587278717752, 0.062520283424960521, 0.0057173191551838087, 0.0088721340546120686, 0.023671425316321493, 0.063347137679256704, 0.012075913730590138, 0.028861223024956306, 0.024588721701057192, 0.52109828163477667, 0.0022509219933257718, 0.029543575650353482, 0.012539121436934142, 0.059655200546542275, 0.0030095720122584879, 0.015964650492634735, 0.030874258762874085, 0.054338934925999283, 0.48028402594362118, 0.027869501151299048, 0.034229714355880514, 0.063690639279931016, 0.0036070991986192347, 0.029176646768805714, 0.019830009818129657, 0.052428110119433047, 0.0049477795808519076, 0.52956749300893691, 0.030852207467170434, 0.046552415619032228, 0.0068086658829740188, 0.024180920129256656, 0.035282703599617271, 0.057983816294609802, 0.0098494159741209231, 0.025333090707472028]
sEMT_Cu_Rasm = [0.058643605601085669, -0.040590194790239821, -0.0070128000505815091, 0.0083031717994300636, 0.0029582231616937199, -0.024859105138712437, 0.0072595507256171012, 0.039913357916079993, 0.028558893078442355, -0.011730249246911222, -0.011392740517664065, 0.018402700035659546, 0.014395831048064557, -0.028928910549818155, -0.0082908567789256819, 0.011219245157591259, 0.015232741714548345, -0.022629617121776545, 0.020700598397121999, 0.023109676968683917, 0.023013670452065978, -0.013393335499594644, -0.017954307364461349, 0.014676368442481293, 0.01830756009248307, -0.035506665614238611, -0.00361911045123719, 0.0079811017623495819, 0.018126344234873953, -0.018948772398271484, 0.013775838546452994, 0.03302333738329806, 0.021204249893687212, -0.015929423597862674, -0.021492212897841898, 0.0093935473499187939, 0.036419681710143814, -0.034948927260674903, -0.0020899578571053519, 0.018074400064718742, 0.019652623290055782, -0.014433339357595582, 0.016121690050861961, 0.036754125718598978, 0.017762921742180471, -0.016937390333969356, -0.023139742605754052, 0.0041682253679168509, 0.018549862363376638, -0.03450890811811308, 0.0011191184601937526, 0.019189184419112628, 0.01987508513654325, -0.0093625084448677592, 0.048620995860338974, 0.036552794081245427, 0.011516907973478952, -0.020657042219557123, -0.023313613912442997, -0.0016027272974334474, 0.015081796796767705, -0.029043498487057878, 0.0049417685855804193, 0.010622710165397887, 0.019365604591089353, -0.0030497513654179232, 0.017562729374177272, 0.037528244142050374, 0.0055721343896520852, -0.023136289078657554, -0.021994061622037323, -0.0077505377524057593, 0.012821929840533762, -0.022125096479533153, 0.0062669618461665627, 0.016621526040894574, 0.017046066586199605, 0.0035365795746653303, 0.017063202928911475, 0.034004210472117088, 0.001237699050835809, -0.016741688693002844, -0.019702752530286471, -0.012801358833978557, 0.0047961473704059721, -0.013641336795803564, 0.0082609960190525127, 0.013999654100096268, 0.014345742281179867, 0.010627020030530355, 0.065787643883006661, 0.028223050323842605, -0.0037219635481970368, -0.024323169158177067, -0.015628911511115028, -0.017630013916718774, 0.00076955662353940957, -0.0058969970156792098, 0.01078234557618042, 0.0069808874444052607, 0.011393874685691743, 0.016226245708345251, 0.013967724383165629, 0.018468685504180942, -0.0064280257254605887, -0.021463078646007296, -0.010684805932005883, -0.021682257419634546, 0.0014264105675308187, -0.0022584814300829793, 0.01291796296053529, 0.006186500258171931, 0.0064233182642679529, 0.020629466204244003, 0.012224344510234813, 0.0070050399322049203, -0.0066316090228109928, -0.0077291865851378738, -0.0049444153365094945, -0.02421320772774899, -0.00077709674972930773, 0.0071698930135572873, 0.015866911067140468, 0.0013763404777389716, 0.0016076556558877258, 0.023241790859486171, 0.065565853347884659, 0.0021906119540935098, -0.0084879990789463334, -0.0088192341204704188, -6.1649258081143403e-05, -0.020900784086085242, 0.0055937217212043483, 0.012071262958380357, 0.018807472352800177]
eEMT_CuAu3 = [0.60617514732652422, 0.28418658487861181, 0.28475591414046963, 0.29135426219928773, 0.29557596769516836, 0.28135332481569808, 0.28658829784071482, 0.28895487031285194, 0.29783047958434405, 0.61092479816321443, 0.29000226517749628, 0.29087498250346799, 0.28768358998776833, 0.28734066053444574, 0.28617041281018807, 0.29337732031075614, 0.2921293673322567, 0.28991525885731573, 0.6011521220303031, 0.29010457766215803, 0.29254341221227165, 0.3024243099880799, 0.28517862881155898, 0.29233483253082593, 0.28853878634793473, 0.28714573529345477, 0.28808496351203194, 0.60613359950743773, 0.29238532568080977, 0.28706009211218664, 0.2838638384315213, 0.29344115314416008, 0.29107390818699486, 0.30005477658565693, 0.28507562009321452, 0.29657489927174385, 0.60310887531218249, 0.29136318224541391, 0.28516306518603152, 0.29455134854749021, 0.29017178693004242, 0.28677745241874275, 0.28471241099622357, 0.29460624894551835, 0.29235482123345502, 0.60917027449692895, 0.28714413422597396, 0.29485067273505328, 0.29396422172048098, 0.28659235158667551, 0.28580848614200516, 0.29313721491152878, 0.28905262388629893, 0.28924271446384608, 0.5977708967824733, 0.2929662166710032, 0.28876184837636076, 0.29192256833048713, 0.28662731929061902, 0.29503839082554162, 0.29801377126285411, 0.28627156340980875, 0.29008617302669526, 0.60556624474339538, 0.29160211467686237, 0.28615737939081676, 0.28937783798922556, 0.29477122011160661, 0.28804864642908301, 0.28813890916714024, 0.28833679083629704, 0.29710359586963575, 0.60973525094433612, 0.289877652360782, 0.28900585283396252, 0.28916605857716071, 0.2877167070555795, 0.28571706208821768, 0.29209432905742494, 0.29386211604596468, 0.29018714485429387, 0.60283346771267254, 0.28924597116692263, 0.29346438125176633, 0.30278523637762689, 0.28542175882322018, 0.29103778820365545, 0.28825007781128598, 0.28734562078116799, 0.28824395926769109, 0.60469628754096716, 0.29270526156824372, 0.28725296806389133, 0.28403331163517276, 0.29232359663095142, 0.29205128763019284, 0.30187211214811915, 0.28509936784633005, 0.29562368229832447, 0.60238081900096185, 0.29148883532227732, 0.28507308006774323, 0.29484115729695137, 0.29108357267781582, 0.28695848520382716, 0.28400069605960754, 0.29389485104272772, 0.29320800841391748, 0.61006805663654795, 0.28735631609728784, 0.29429814195161708, 0.29149048940892675, 0.28677960856646223, 0.28529064915510549, 0.29420200379798089, 0.2897719503168501, 0.28939777673707656, 0.59730434486595962, 0.29252459696406286, 0.28945884786759279, 0.29486267732830429, 0.28573646922217399, 0.29495926529342809, 0.29531734419302413, 0.2865844684540102, 0.289091122470857, 0.60516659302143605, 0.29043863583824781, 0.2871542963720275, 0.28850865838136652, 0.2932209053900765, 0.28773771269522586, 0.29113356529309131, 0.28893717566569954, 0.29570111903995766]
sEMT_CuAu3 = [0.055378046054133025, 0.062781877381923187, 0.056125889882997271, 0.002146817001082778, 4.7269920373667129e-05, 0.0027411654334203585, 0.05822439434362945, 0.062965621635873534, 0.060955857037688174, 0.0055914444231161889, 0.00090323790881225319, -0.0042320233630307362, 0.056148376571817149, 0.055891691449085817, 0.056568648379554679, 0.0023012678567395748, 0.0017058110768916057, 0.0024870335323893991, 0.023884427459889706, 0.066794349021190538, 0.056875403337259635, 0.0028596243819698501, 0.00043709551487638033, -0.0038357931914647925, 0.057748812478610009, 0.055878613523429578, 0.060529656446697083, -0.0018851865346705546, 0.0017367307146460432, 0.0024871785203170282, 0.056926804363162983, 0.054762640306729719, 0.056433542570967429, 0.0023201986541817872, 9.9710508625948114e-05, -0.0030129170733241319, 0.041735119762020864, 0.065587694711607136, 0.05952670693323979, 0.0017337697687432913, 0.0017142435726393989, 0.0022341698815369969, 0.055992855766431919, 0.053962336175190244, 0.057747775684051338, 0.0044545893906007845, -0.00026327390501212, -0.0019809508507115468, 0.058642716525600082, 0.056686074881300043, 0.0604436163529046, 0.0012789716030239722, 0.0013167534205275572, 0.0017097135991535088, 0.044617942186424127, 0.065150544051018819, 0.055050994384874034, 0.00060544361099211421, -0.0010406629616944083, -0.00085076290779087949, 0.05811598017104664, 0.057496934686496602, 0.062954889687546797, 0.0011611943730128378, 0.00069066680437883756, 0.0011899369212640925, 0.053597476843247033, 0.053850558568096542, 0.054233677183266889, -0.00018325535635417336, -0.0016199855407386327, 0.0001910597003853788, 0.024432369160518934, 0.067317678776232917, 0.060739302114503908, 0.00025892937181356987, 0.00041723564382929339, 0.00044642232069622503, 0.052403217670511128, 0.054382945023529888, 0.05566742868195191, 0.00086687369377515993, -0.0019871826559978629, 0.00088445675195053097, 0.056906961254187108, 0.059427520582629179, 0.06019429517070491, 5.7927134914350501e-05, 0.00014843207614608474, -0.00043528347414660177, 0.061093109804306926, 0.066725946848115836, 0.053135376203653661, -0.0009124872376655008, -0.0020677180994888543, 0.001388882514941356, 0.056887362288151028, 0.060169803934459733, 0.061324573061604291, 0.0036903683871572271, 7.1719891987807817e-05, -0.0013196991472529795, 0.051191843198314636, 0.055684448228556116, 0.053046684695041146, -0.0007481872865794276, -0.0017330820521737765, 0.0017270574644623904, 0.014867318688427011, 0.069599216324098101, 0.058699446414140558, 0.00079847120780158327, 0.00012211975430207394, -0.0022663255868956207, 0.051522696607690682, 0.05608197164639591, 0.055646029688443351, -0.0020815161574036065, -0.0011113252956336769, 0.0019787320035738135, 0.057811071225686989, 0.060134456193097284, 0.058121785118331534, 0.001600373512125171, 0.00028915937211140163, -0.0031374247182117238, 0.063859419186069299, 0.066389146719553108, 0.05466305358007674, -0.0015014627511628856, -3.5318882327516526e-05, 0.0028074110890584938, 0.058093915096317866, 0.060069544756794019, 0.058432318292342231]
eEMT2013_Pt = [0.70632625243267277, -0.007415804523741798, -0.0026115457517814633, 0.016865268556049529, 0.0052747052782748938, 0.027722647947615364, -0.018787906854611514, -0.025547182110432054, 0.010980317639855741, 0.64181535824282587, -0.024322169798429272, -0.0097088382670049711, 0.01746208016297679, 0.016303856070800649, -0.009802626109036261, 0.052577437799914861, 0.0087094175034838628, 0.016625553795794445, 0.62784520550419209, -0.026111899576775066, 0.011369862209576809, 0.030675727761054539, -0.01806787292980605, -0.0016069070468756053, 0.0089435596847726728, 0.014868672204134015, -0.016240371182918878, 0.75974148926886009, -0.012591713176389518, 0.013822447838038876, -0.016763531751261773, 0.0035378333810092144, 0.011599921721824558, 0.021202700975382349, -0.023626609818030886, 0.011938352577255174, 0.65496586810890545, -0.0079376939784516765, -0.02484962501323551, 0.072234746096587088, 0.012525199109580498, 0.0095311392853361099, -0.0084071340905769176, 0.0091943893963915002, 0.016249184673380768, 0.62818418890680405, -0.041583180631743488, 0.010503224823610324, 0.012111246176537804, 0.0060801551125813091, -0.02621577582595247, 0.064814069555693798, 0.014628756298337819, 0.005102466848723175, 0.66495699512693918, -0.014291315796108428, 0.015404062451263023, -0.0065084591494271038, -0.024675349537057301, 0.012441045872355616, 0.021622934504135216, 0.00018606972234369579, -0.017039390191369463, 0.73466495149844313, -0.0048045607372815269, -0.0019076049728807831, 0.021680384274169739, 0.012612250474917097, 0.017092987924605119, -0.016545044346781168, -0.018952948295319239, 0.017688922756097014, 0.64262480387164622, -0.022921350349746739, -0.016288214956990288, 0.030744097974515938, 0.01749296465596295, -0.0087675100804318618, 0.041662434214307709, 0.011958485704478328, 0.018247130405312006, 0.62558393786487798, -0.030642666537405105, 0.011724933357261769, 0.033056865509694333, -0.013475603075502107, -0.0075435083697650285, 0.015354257506635882, 0.016569174416323662, -0.012542265840611577, 0.74742211496676081, -0.013417998347202698, 0.015875924046635959, -0.020022921247357495, -0.0016789203418374754, 0.011244792343275023, 0.028318344574656429, -0.020096966757477297, 0.0073806030632193043, 0.66322890425650805, -0.0057345704582436596, -0.021928858148226205, 0.070930525460723537, 0.01159317227401413, 0.012534073442987292, -0.01449730191676224, 0.0056963006578421016, 0.01558174675458357, 0.63065020964881757, -0.039986166624150776, 0.0076528472957111404, 0.0077157128453615442, 0.0095609075183507031, -0.025786688329648477, 0.070977295012506936, 0.013157968357835337, 0.0084991051348071167, 0.65063219186990917, -0.0158592699689315, 0.01399473206905455, 0.003191501085938242, -0.026451228810228322, 0.010927022372063, 0.01480745988911103, 0.0049595715370180926, -0.020193456898486062, 0.74640128503815095, -0.0025278073812078361, 0.0014036501272816082, 0.0037267834529464139, 0.0088816044477413314, 0.023289915667813688, -0.010595632040512726, -0.024279651394340185, 0.015295325796308212]
sEMT2013_Pt = [0.10120703221359158, -0.0094171560709612485, -0.025083432683556756, 0.0068112240290219171, -0.0024131902642881378, -0.004432292607453368, 0.0040775915192829493, 0.028444601273722482, 0.015839072909498948, 0.0071397001067645119, 0.0015049285307563013, -0.0042810384937465411, -0.02202440475513923, -0.023259696766317246, -0.026069308385950455, 0.0035899314938915147, 0.004495849716285364, -0.00038618203934135049, 0.03258099805986072, 0.029019529668864744, 0.0017135370176847256, 0.0074122718774031343, -0.0013455439225197291, -0.0044957045481493069, -0.015070795755554431, -0.026296104516036624, -0.0088772239791913773, -0.001218582645794533, 0.0052750159037476159, 0.0019615192713681711, -0.0047540979524866474, 0.002976338807142286, -0.0013658047105663935, 0.0063148943179897887, -0.0035383691337939772, -0.004098900901662028, 0.056937147496391761, 0.0034290887392654868, -0.012691171500381465, 0.0067407541509570913, 0.0069146212373868005, 0.0036298266763637385, -0.007641756248733797, 0.00236993086323573, 0.0028922891844300868, 0.0089057502221695107, -0.0050207678754174718, -0.0034422582341319106, -0.0069625100268579801, -0.027835703013804388, -0.0063352195957212427, 0.0071793147144836806, 0.0075618298678841343, 0.0043757817863077694, 0.085305919788680296, 0.02849213212957756, -0.010657796790155334, 0.00066403251228599601, -0.0075678533072470328, -0.0027478642437731809, -0.0056845486059998018, -0.026550296029124967, 0.0082523776296348581, -0.00018914290746969206, 0.0072159521274538395, 0.0045457721517596006, -0.016864907150633227, 0.0013913064396244791, -0.016157187555480935, -0.0031877404246961954, -0.0089283739357330846, -0.0022273737960429303, 0.018831762099297763, 0.0058916089434292284, 0.0029082409320127234, 0.0048785106609606707, 0.008410674334328112, 0.0038618005279209464, -0.023392950373017224, 0.00057314582086528368, -0.011363614365553592, 0.0039481218999047009, -0.0087359258513643803, -0.0024943729019561494, -0.0052156729864994561, -0.019984427954981496, 0.0048323350951969095, 0.0033470325908997261, 0.0084463736630728571, 0.0026506678590081096, 0.13026663118012863, 0.028276925996823059, -0.025276307710172037, -0.0095787060147356912, -0.0089215286219197689, -0.0030066520707048203, -0.0042130845989299245, -0.014828857167788029, 0.013348866747693035, 0.00051741827230547511, 0.0073938976591136395, 0.0013530276563568735, -0.034525100697924145, -0.0041014757804197916, -0.028393617922922151, -0.010628024929564489, -0.0072533905983750311, -0.0036167753389277002, 0.0076209733551589809, 0.018714270132120129, 0.0056103373662636583, 0.0027566363397871856, 0.0069477128875769035, -9.8381997801465291e-05, -0.036106702148032528, -0.0082158008183530699, -0.019607675134243999, -0.0011940923422757562, -0.0043996800728655396, -0.0040869263932764716, -0.00058905990304401181, -0.0039038193826160827, 0.0051141209516759913, 0.0040768622089300361, 0.0054617798389962162, -0.0015918732826044298, 0.12988620354710032, 0.010204947948129418, -0.027664050726620044, -0.0089682164060197363, 0.0012320151121547713, -0.0028836769865239181, -0.00021728520134952091, 0.0072480683589705259, 0.0065633578432624795]
eEMT2013_Y = [0.81952362225852049, 0.10025623624130464, -0.08483233069553453, -0.1199491497887859, -0.10791856620622209, 0.014327079535898513, -0.098992007404246074, -0.17445450019611819, -0.078648494883930553, 0.78239089306233467, -0.015120894105097982, -0.13485353319603366, -0.09549580418557202, -0.01285177532807058, -0.10247934428310135, -0.11716397505814591, -0.088665825654252295, 0.033370265567785218, 0.76702659686796082, -0.076419208238656999, -0.084282512841019397, -0.03882911821752888, -0.11876555732955385, -0.12550074604526262, -0.098934796489424492, -0.0091585532011526638, -0.0888254759218432, 0.82171486575933717, -0.01171031100302411, -0.010873753166163347, -0.10868455348304185, -0.11923546849879951, -0.072829857850178037, -0.032986484339583733, -0.13460869627247352, -0.097515733320796549, 0.79353255346042406, 0.073745021166039315, -0.13825748299343399, -0.095867175568799645, -0.06308618066130034, -0.021966445959599845, -0.12033746961771996, -0.1110760191165765, -0.025285582419907193, 0.78180428394976076, -0.075438046280408066, -0.10861201398686848, -0.092683403611369286, -0.033679284470463422, -0.14500675810092289, -0.089588622645276672, -0.046367869311733756, 0.0043581051718142305, 0.77175481331629214, -0.055360200810294025, -0.040544469202294486, -0.045881150804667037, -0.14561418356706746, -0.10265889915500015, -0.079881841532607467, -0.055890354526801467, -0.11694216685910153, 0.83306433670100954, 0.054521518779810485, -0.063978754507701296, -0.12621162649399231, -0.098953969839644884, -0.024750097024027973, -0.061846809463440344, -0.14181913952693481, -0.077349427718526265, 0.7847481083332406, 0.0027328187619728439, -0.13953080398443962, -0.091346542026816913, -0.016320665274193402, -0.089184591160187843, -0.1209676038313523, -0.092774146080491171, 0.030510481491523578, 0.76960153800755204, -0.080019622863473749, -0.09022027756129436, -0.047387417528974574, -0.10487882695673001, -0.13147293413243766, -0.096477037937710897, -0.0092544375578098581, -0.074355591192496462, 0.81243183543809483, -0.023444381558340943, -0.0086807372595654186, -0.098214661148380067, -0.1253227745513259, -0.081110854661187837, -0.036200693807518114, -0.12464130979460641, -0.10227101769985669, 0.80013675280688101, 0.08047313979543258, -0.12984364320991659, -0.10204252208507558, -0.072925652312386013, -0.013667511826404244, -0.11305785971806781, -0.11635618722643226, -0.038669511381526966, 0.78360738351648074, -0.066983999246583714, -0.11354628973215775, -0.097853528548190738, -0.021848457220567497, -0.14134729531622003, -0.093352140503645487, -0.057775300096455595, 0.018616945537616836, 0.76864302517814576, -0.061554594038887522, -0.051908483242885772, -0.035265974185332283, -0.14572158063015461, -0.10792065110503124, -0.089101692356882367, -0.037678348808458217, -0.11676170837527255, 0.81555097794556097, 0.030623984694483575, -0.050977241191085376, -0.11507324855552259, -0.10336720869406335, -0.043510640167919057, -0.062992926470976762, -0.15049747704443739, -0.080840373260410381]
sEMT2013_Y = [-0.01798281531617589, -0.053447046083923401, -0.018097266038247899, 0.0036120100074414326, 0.00036935335197616035, -0.0091611848816469735, -0.011308772416406607, 0.0025606185018321004, -0.015831680587954731, -0.00066385311333794813, -0.0062077924003013443, 0.0074527185505898512, -0.021514676898446737, -0.029977347282134144, -0.020049709045760148, 0.0021820065610842019, 0.0069845892650629293, -0.0090464864608079554, -0.014791832246941082, -0.016190773665224322, -0.012307144608516294, -0.0022783428746377967, -0.0089455723454837672, 0.0059312617562805011, -0.01935352095841807, -0.030836151354778515, -0.022935029452538728, -0.00013211498680166153, 0.0093344433480663045, -0.0063268487768899104, -0.0085493113290765234, -0.0033596116026147508, -0.012903890554873789, -0.0043975410291046818, -0.010590025804010679, 0.0049173450879645845, -0.018083415651684358, -0.045423395146481763, -0.018244334711855797, 0.0074697251187767419, 0.010631384821148459, -0.0043615745342384365, -0.0092819776971257238, -0.0030875917917705656, -0.0174501348064857, -0.0025400102655879562, -0.011575604468701895, 0.0017115121819867706, -0.016210041946220735, -0.029106304766463132, -0.017348716403604122, 0.0092574900528373111, 0.011274202028724161, -0.002831506120683698, -0.014913184595432878, -0.015975423312231618, -0.015250759710659267, -0.0086373326043706761, -0.011467497448900165, -0.00075626604035886644, -0.015184197256079284, -0.026793369005425789, -0.019463165527123863, 0.00073027291541868358, 0.011248382197261399, 0.00019818761643349217, -0.013000239926772589, -0.0053725288053525257, -0.016662205685877486, -0.010500167350553999, -0.010800163241183268, -0.0032716114667669027, -0.01632138590479636, -0.037503998465874246, -0.01567757763976035, 0.010197271258197841, 0.010373315892095978, 0.0026301586503714412, -0.015594026722609197, -0.0079753365668285853, -0.022353782205860942, -0.0035318240917848217, -0.0095309657618851008, -0.0055873488702811195, -0.014014341469433778, -0.02065362733635185, -0.014962955277219516, 0.0095954820825590124, 0.0088353405263432612, 0.0051606288383724977, -0.016606192059268853, -0.025421620498678046, -0.018977210134665825, -0.012265760040008471, -0.0075503314172941276, -0.0075486548713966399, -0.01347024681445232, -0.017494439796454285, -0.016616786185729666, 0.0017018555992147895, 0.0067250513625765193, 0.0068109948665271477, -0.020517983234820351, -0.015227024924013989, -0.019685830411294094, -0.011624208787484979, -0.0051025892091187165, -0.0096995639598973209, -0.015123454535057949, -0.027115778941130989, -0.013605030323662349, 0.0068317061380534349, 0.0038456867785596409, 0.0081477871183003574, -0.022153379467308085, -0.019386352564178262, -0.024735351068725514, -0.0021779676205882677, -0.0022232137432876033, -0.0098334897745191718, -0.011696036500221132, -0.01168965172704952, -0.012810790471109782, 0.0049689967540736072, 0.00080909896623110745, 0.0099991851963078509, -0.016711085406240146, -0.038552727194459943, -0.019051054466322173, -0.0073633184829835158, 0.00061639559741062016, -0.0077611764520759277, -0.010184705943725877, -0.0074272598107294179, -0.016724169335423582]
eEMT2013_Pt3Y = [-2.3657824608080276, -5.4798030334711081, -5.6181843975748267, -5.6235389918681156, -5.6509989581516349, -5.6077208957270939, -5.6170844358759906, -5.640226649869617, -5.6159591242298772, -2.7103744299861994, -5.5301681727274987, -5.6344803264898706, -5.6385597908886593, -5.621957322605339, -5.6298323133432726, -5.6146197609616832, -5.6269190177720914, -5.5969080713880492, -2.6437738648779554, -5.5491913667352799, -5.6351162275784281, -5.6129037214073767, -5.6281236586184233, -5.6296764772637067, -5.6490389783130661, -5.6249842214450547, -5.601746602476001, -2.268045520557199, -5.5200525065129833, -5.6245943943564916, -5.623063212609245, -5.6314602109105527, -5.6344636445452592, -5.6093862946972868, -5.6277420950568837, -5.5967997472815503, -2.5383203811473534, -5.497697261333319, -5.6275726103029102, -5.6159056908199139, -5.6328971861964119, -5.6254162603678557, -5.6227267060934265, -5.6335133165878899, -5.6008612160649429, -2.7299065944916112, -5.5421073033946806, -5.6342791371985745, -5.6451756481588715, -5.625829331610869, -5.627611122735817, -5.6214647121881098, -5.6298968945948369, -5.6030694286521259, -2.4644802548231706, -5.5456433638633955, -5.6290140425782456, -5.6125445288968132, -5.6273205337120116, -5.6364531587179334, -5.6366737298686251, -5.6262340930777954, -5.5961736023312527, -2.2958992847718598, -5.4965482567323418, -5.6263814402944421, -5.6180623087883186, -5.637117357819684, -5.627310560504502, -5.6163841238401817, -5.626850470977879, -5.6008485167908377, -2.6904910242432827, -5.5194857051978881, -5.6269809888740658, -5.6384199218709972, -5.6262637308379793, -5.6275974946025764, -5.6151603180504539, -5.6368278372617224, -5.6004057106468386, -2.6717148562933728, -5.5489126840552023, -5.6366463465409717, -5.617352866785768, -5.6279450824334054, -5.6285599649420623, -5.6459395714332077, -5.6249558498630874, -5.6028255323736866, -2.2898731662952416, -5.5260251228683464, -5.6247115904741749, -5.6223167070166609, -5.6298625161666314, -5.6358315516747721, -5.6112596044270413, -5.6278010084310486, -5.5958034890485129, -2.4900385991079048, -5.4946125606673055, -5.6277014001727759, -5.6138985265819192, -5.6345130260987153, -5.6251604011429839, -5.623122742108845, -5.6318620102526955, -5.6011892714924132, -2.7311269778003764, -5.539322006646322, -5.6326275741062739, -5.6487396608742459, -5.6254620660915142, -5.6279885678923618, -5.6173489171557778, -5.6315812720329559, -5.6025710807649842, -2.5098309387902544, -5.5488369476014432, -5.6294046299876923, -5.6100875208732832, -5.6291893602670386, -5.636328924807855, -5.6422717359616152, -5.6243245030490554, -5.5990518980916333, -2.2815815033859916, -5.502690081701906, -5.6336303262123151, -5.6014759906675744, -5.6234027059942813, -5.6349252153668088, -5.6187231618960842, -5.6235218122977519, -5.5873275084217129]
sEMT2013_Pt3Y = [0.019249197151650858, -0.016930509714478049, -0.031299879440062718, 0.00012415539687496608, 0.0004135301579808657, -0.007091744186387406, -0.018349943984978252, -0.010442825901286907, -0.0081090054609319357, -0.00037244041062622771, -0.0041834726024571446, 0.0076293345625553519, -0.029180190640773138, -0.032720705417666945, -0.025992867473438201, 0.0016526092094350099, 0.0056930601101264763, -0.0052535569569804527, 0.011632118636144008, 0.0044262319766986196, -0.019441761637717953, -0.0003448504184219264, -0.0061523705598177962, 0.0053762604712580125, -0.026959907272724185, -0.034432623324463944, -0.019621541548801302, -0.00025813636318764181, 0.0069530921366097948, -0.0031641413969817787, -0.01802537862271289, -0.016906805703692466, -0.019802197503199833, -0.0014854011917682147, -0.0075479514783475324, 0.0021575010293971458, 0.015084917963698043, -0.015322157957416187, -0.025048637950898664, 0.002908590325416619, 0.0077836041384900072, 1.3089855960307776e-05, -0.01867382930814512, -0.017548113658731972, -0.014747104784863517, -0.0035204202885660055, -0.008592369760697955, -0.00010741640575852888, -0.025457585275341164, -0.033811317502202502, -0.025142041080059199, 0.0037274491915674926, 0.0079895629363605954, 0.003282019520970768, 0.017745337988624554, 0.0042419936812218891, -0.021356993417768942, -0.0035488548776060436, -0.0090362955197188649, -0.0030745087610346412, -0.024787269005349073, -0.03210015758720499, -0.020096030767893725, 0.0038543453597490603, 0.0076307852484601918, 0.0056877040875486125, -0.021197177400165787, -0.020001786249802381, -0.022410246637195159, -0.0043480575131517275, -0.0088885301206964289, -0.0057840318510042118, 0.0075967468670278303, -0.011279042787097163, -0.024922122988022245, 0.004470796025003082, 0.0068067518880782756, 0.007803453133632501, -0.022886572834143078, -0.021521509787898914, -0.017560119786129147, -0.0047797304569715347, -0.0079947681344637884, -0.0083644825899576395, -0.023257658274831783, -0.027177552792324349, -0.024468126967363467, 0.0044440494599490375, 0.0055713336320723185, 0.0088815120012156711, 0.022733572100206035, -9.1040694632402213e-05, -0.024154954269260689, -0.0050871648324585907, -0.0066374273494523737, -0.010268261226402293, -0.022275781457229943, -0.024400188654416108, -0.018736401545304378, 0.0049765088037499313, 0.0040664843697514946, 0.010238623198991728, -0.026232493040592501, -0.02530513010570349, -0.024679110256835352, -0.0048485856565905032, -0.0046354573981929308, -0.010590191540105407, 0.0047818318945192749, -0.0031361532334183259, -0.022701521336404202, 0.0037185489712712799, 0.0022312990915299815, 0.010575455694489928, -0.027444938287929852, -0.027322427156237186, -0.019182650778041335, -0.0046971999364225801, -0.0020733058637669903, -0.011728282130790376, -0.020013317717179249, -0.019805399931756101, -0.022045173905919483, 0.0031930550911606595, 0.00037267338684092677, 0.0094867654877828084, 0.024353554499900041, -0.0062327163075974641, -0.022877738476485995, -0.0033712876725920903, 0.00081120245053026632, -0.010987933030608892, -0.017839230192141186, -0.018668688319740237, -0.017058819288402759]
if __name__ == "__main__":
    print("This is not a test, but a module containing test results")
