import re
import os

# Placeholder for Newick tree string
newick_tree = "(scerevisiae:1.748595,(celegans:2.17059,(dmelanogaster:1.87330,((csavignyi:0.40965,cintestinalis:0.38850):1.18479,((pmarinus:0.90389,eburgeri:1.06454):0.23348,((ecalabaricus:0.35246,(loculatus:0.23849,((sformosus:0.21138,pkingsleyae:0.24326):0.08116,(((dclupeoides:0.25003,charengus:0.28819):0.05295,((drerio:0.13515,(sgrahami:0.07646,(cccarpio:0.05125,cauratus:0.06721):0.01241):0.04334):0.13317,((ipunctatus:0.20970,eelectricus:0.20364):0.01893,(pnattereri:0.11423,amexicanus:0.14426):0.04191):0.06635):0.06673):0.04466,((elucius:0.14328,(hhucho:0.07284,((strutta:0.03054,ssalar:0.02819):0.02014,(omykiss:0.03049,(otshawytscha:0.06502,okisutch:0.02628):0.00819):0.02176):0.01095):0.06870):0.10052,(gmorhua:0.33286,(mmurdjan:0.13332,(hcomes:0.30190,((tnigroviridis:0.15592,trubripes:0.11608):0.15308,((csemilaevis:0.25972,(((marmatus:0.12740,(bsplendens:0.15599,atestudineus:0.08672):0.03304):0.01406,(smaximus:0.14066,(lcalcarifer:0.07699,(slalandi:0.02792,sdumerili:0.02184):0.05967):0.00756):0.01392):0.00751,((lbergylta:0.15734,(saurata:0.11251,(lcrocea:0.09897,dlabrax:0.08154):0.00821):0.00872):0.00768,((gaculeatus:0.14228,clumpus:0.10441):0.03780,(slucioperca:0.08656,cgobio:0.12936):0.00853):0.02321):0.01448):0.00582):0.00465,(((spartitus:0.08211,(apolyacanthus:0.05688,(apercula:0.01671,aocellaris:0.01891):0.02997):0.03546):0.04337,(acitrinellus:0.07825,(oniloticus:0.03234,(nbrichardi:0.04473,(hburtoni:0.01994,(pnyererei:0.01964,(mzebra:0.01023,acalliptera:0.01372):0.00848):0.00422):0.01233):0.01575):0.05431):0.06416):0.00842,(((osinensis:0.05575,olatipes:0.03239):0.05956,(omelastigma:0.05090,ojavanicus:0.06001):0.03395):0.15431,((nfurzeri:0.17534,kmarmoratus:0.13739):0.02770,((fheteroclitus:0.12894,cvariegatus:0.13664):0.01468,((xmaculatus:0.01610,xcouchianus:0.06750):0.03269,(preticulata:0.04259,(platipinna:0.01556,pformosa:0.01381):0.02881):0.01777):0.07401):0.06998):0.02640):0.03407):0.01825):0.01343):0.01389):0.04848):0.03763):0.08163):0.07031):0.06677):0.10576):0.08968):0.10034,(cmilii:0.47576,(lchalumnae:0.33449,((xtropicalis:0.21895,lleishanense:0.28375):0.20894,(((spunctatus:0.16529,((pmuralis:0.12547,smerianae:0.15793):0.01835,(acarolinensis:0.18259,(nnaja:0.04354,(llaticaudata:0.07489,(ptextilis:0.02870,nscutatus:0.03475):0.00916):0.01176):0.18284):0.01693):0.12003):0.02605,((psinensis:0.10579,((tcarolina:0.02414,cpicta:0.02244):0.01180,(gevgoodei:0.02738,cabingdonii:0.03236):0.01544):0.02847):0.05663,(cporosus:0.14899,(scamelus:0.08460,(((abrachyrhynchus:0.02796,applatyrhynchos:0.04712):0.03987,(cjaponica:0.04881,(mgallopavo:0.06142,ggallus:0.03482):0.00686):0.05808):0.02316,((shabroptila:0.07414,acchrysaetos:0.04313):0.00827,(pmajor:0.04649,(falbicollis:0.06065,(tguttata:0.04687,(scanaria:0.03905,gfortis:0.04666):0.01854):0.01242):0.00477):0.07765):0.02036):0.02412):0.09169):0.02608):0.02560):0.06855,(oanatinus:0.24627,((mdomestica:0.09095,(sharrisii:0.07706,(neugenii:0.17280,(vursinus:0.04090,pcinereus:0.04052):0.01681):0.01095):0.01716):0.10891,(saraneus:0.34990,(((dnovemcinctus:0.09349,choffmanni:0.25985):0.02857,(etelfairi:0.27657,(pcapensis:0.19613,lafricana:0.06487):0.01590):0.02193):0.00904,((eeuropaeus:0.30745,((mlucifugus:0.11389,(rferrumequinum:0.06960,pvampyrus:0.10681):0.00810):0.01539,(((ecaballus:0.00953,easinus:0.01449):0.05789,((ssuricatta:0.06244,((lcanadensis:0.01558,fcatus:0.01189):0.00447,(ptigris:0.02604,(ppardus:0.00778,pleo:0.00922):0.00387):0.00603):0.02685):0.02083,((vvulpes:0.01715,(clupus:0.00596,clupus:0.00521):0.01080):0.04578,((mputorius:0.02185,nvison:0.02277):0.03904,(zcalifornianus:0.04367,(amelanoleuca:0.02776,(uthibetanus:0.01003,(umaritimus:0.02177,uamericanus:0.02673):0.00218):0.01281):0.02145):0.00330):0.00832):0.01100):0.02451):0.00386,((vpacos:0.17221,cdromedarius:0.02167):0.04960,((cwagneri:0.04764,((sscrofa:0.01073,sscrofa:0.00683):0.00220,(sscrofa:0.03444,(sscrofa:0.02052,((sscrofa:0.01282,(sscrofa:0.00944,(sscrofa:0.00862,sscrofa:0.00997):0.00263):0.00128):0.00216,(sscrofa:0.01087,(sscrofa:0.01051,(sscrofa:0.00904,(sscrofa:0.01000,sscrofa:0.00790):0.00148):0.00196):0.00162):0.00336):0.00263):0.00284):0.01216):0.03505):0.03591,((bmusculus:0.02690,(pcatodon:0.03414,(ttruncatus:0.05612,(psinus:0.01691,(mmonoceros:0.00782,dleucas:0.00873):0.00695):0.00484):0.01210):0.00425):0.02935,(changlu:0.03491,(mmoschiferus:0.03615,((oaries:0.01416,chircus:0.01621):0.01847,((btaurus:0.00588,bindicus:0.00675):0.00440,(bbbison:0.01892,(bmutus:0.01401,bgrunniens:0.02110):0.00378):0.00283):0.02010):0.00609):0.00386):0.04656):0.01025):0.00614):0.01949):0.00321):0.00506):0.00901,(tbelangeri:0.25648,(((ogarnettii:0.08259,(mmurinus:0.04648,(pcoquereli:0.05042,psimus:0.04063):0.00332):0.02050):0.01845,(csyrichta:0.10557,((cjacchus:0.03187,(anancymaae:0.03452,(sbboliviensis:0.03532,cimitator:0.02901):0.00420):0.00283):0.02384,((nleucogenys:0.03718,(pabelii:0.02039,(ggorilla:0.01986,(hsapiens:0.01021,(ptroglodytes:0.00712,ppaniscus:0.00937):0.00585):0.00331):0.00916):0.00432):0.00852,(((rroxellana:0.00910,rbieti:0.02008):0.01342,(ptephrosceles:0.02408,cangolensis:0.02183):0.00323):0.00540,(csabaeus:0.01721,((mnemestrina:0.01328,(mmulatta:0.00903,mfascicularis:0.01613):0.00438):0.00729,((tgelada:0.00813,panubis:0.01158):0.00468,(catys:0.01548,mleucophaeus:0.02216):0.00272):0.00213):0.00417):0.00621):0.01388):0.01385):0.03290):0.00739):0.00973,((ocuniculus:0.08770,oprinceps:0.21323):0.04798,((svulgaris:0.04795,(mmarmota:0.02277,(sdauricus:0.03561,(uparryii:0.01996,itridecemlineatus:0.02255):0.00292):0.00456):0.03295):0.04079,(((hglaber:0.06447,fdamarensis:0.06785):0.01993,((odegus:0.08214,clanigera:0.05840):0.00942,(cporcellus:0.01074,caperea:0.07571):0.06968):0.01386):0.05310,((dordii:0.12487,ccanadensis:0.09265):0.01307,(jjaculus:0.12337,(ngalili:0.08700,((pmaniculatus:0.05821,(mochrogaster:0.06521,(mauratus:0.06617,(cgriseus:0.00335,cgriseus:0.00592):0.03748):0.01746):0.00471):0.01299,(munguiculatus:0.08343,(rnorvegicus:0.05417,(mpahari:0.03623,(mcaroli:0.02376,((mspretus:0.01243,mspicilegus:0.02085):0.00242,(mmusculus:0.00864,(mmusculus:0.00820,(mmusculus:0.00257,(mmusculus:0.00540,(mmusculus:0.00278,((mmusculus:0.00141,mmusculus:0.00124):0.00259,((mmusculus:0.00194,mmusculus:0.00204):0.00172,(mmusculus:0.00532,(mmusculus:0.00370,((mmusculus:0.00239,mmusculus:0.00213):0.00110,(mmusculus:0.00322,(mmusculus:0.00289,mmusculus:0.00259):0.00047):0.00034):0.00040):0.00054):0.00031):0.00018):0.00047):0.00035):0.00077):0.00549):0.00164):0.00636):0.00973):0.01384):0.02324):0.02637):0.00914):0.04036):0.01949):0.02055):0.00954):0.00405):0.01251):0.00663):0.00264):0.00936):0.00982):0.01033):0.11488):0.04496):0.09348):0.08048):0.08345):0.03816):0.03603):0.25104):0.36758):0.31997):0.30433):1.748595);"

# Function to get available species from files in a directory
def get_available_species(directory):
    species_files = os.listdir(directory)
    species_set = set()
    for file in species_files:
        match = re.match(r'BIP-(\w+)_gene_ensembl', file)
        if match:
            species_name = match.group(1).replace('_', '').lower()
            species_set.add(species_name)
    return species_set

def filter_newick_tree(newick_tree, directory):
    available_species = get_available_species(directory)
    included_species = set()  # To keep track of species already added to the filtered tree
    current_node_species = set()  # To keep track of species within the current node

    def name_filter(match):
        original_species_name = match.group(0)
        species_name = original_species_name.replace('_', '').lower()  # Normalize the name for comparison
        if species_name in available_species and species_name not in included_species:
            included_species.add(species_name)  # Mark as included to prevent repeats
            current_node_species.add(species_name)  # Add species to current node
            return original_species_name  # Keep the original format if the species is available
        return ''  # Exclude from the Newick string if species file not found or is a repeat

    # Replace all species names in the Newick string, excluding any that do not have corresponding files or are repeats
    filtered_newick = re.sub(r'(\w+)_+(\w+)', lambda m: name_filter(m), newick_tree)

    # Clean up any resulting empty parentheses and trailing commas
    filtered_newick = re.sub(r'\(\s*,', '(', filtered_newick)
    filtered_newick = re.sub(r',\s*\)', ')', filtered_newick)
    filtered_newick = re.sub(r'\(\s*\)', '', filtered_newick)

    return filtered_newick
# Example usage
directory_path = "results\BIPS"  # You will replace this with your actual directory path
filtered_newick = filter_newick_tree(newick_tree, directory_path)

with open('BIP-phylogeny.nw', 'w') as file:
    file.write(filtered_newick)

# You can save 'filtered_newick' to a file here if required
