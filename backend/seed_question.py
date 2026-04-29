import sqlite3

# ✅ SAME DB NAME AS main.py
conn = sqlite3.connect("interview.db")
cursor = conn.cursor()

# ✅ CREATE TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS mock_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    section TEXT,
    q_type TEXT,
    question TEXT,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_answer TEXT,
    points INTEGER DEFAULT 1
)
''')

# ✅ CLEAR OLD DATA
cursor.execute("DELETE FROM mock_questions")

# ✅ QUESTIONS (ALL HAVE EXACTLY 10 VALUES)
questions = [

# ---------------- NUMERICAL ----------------
("TCS", "Numerical", "mcq",
"A train 150m long crosses a pole in 10 seconds. What is its speed?",
"36 km/h", "54 km/h", "72 km/h", "90 km/h",
"1", 1),

("TCS", "Numerical", "mcq",
"A sum becomes ₹1200 in 2 years and ₹1320 in 3 years at simple interest. Find principal.",
"₹800", "₹900", "₹1000", "₹1100",
"2", 1),

("TCS", "Numerical", "mcq",
"A boat travels 30 km downstream in 2 hours and upstream in 3 hours. Find speed of stream.",
"2 km/h", "3 km/h", "4 km/h", "5 km/h",
"1", 1),

("TCS", "Numerical", "mcq",
"If 20% of x equals 30% of y, find ratio x:y.",
"2:3", "3:2", "4:5", "5:4",
"1", 1),

("TCS", "Numerical", "mcq",
"A can do a work in 12 days and B in 18 days. How long together?",
"6 days", "7.2 days", "8 days", "9 days",
"1", 1),

("TCS", "Numerical", "mcq",
"Average of 10 numbers is 50. Replacing one number with 100 increases average to?",
"55", "60", "65", "70",
"1", 1),

("TCS", "Numerical", "mcq",
"Compound interest on ₹1000 at 10% for 2 years is?",
"₹200", "₹210", "₹220", "₹230",
"1", 1),

("TCS", "Numerical", "mcq",
"2/3 of the balls in a bag are blue and the rest are pink. If 5/9 of blue balls and 7/8 of pink balls are defective, find the total number of balls if the number of non-defective balls is 146.",
"216", "649", "432", "578",
"2", 3),

("TCS", "Numerical", "mcq",
"In how many ways can 4 particular persons A, B, C, D and 6 other persons stand in a queue such that A stands before B, B before C and C before D?",
"6!", "7!", "1006×6!", "1004×6!",
"1", 3),

("TCS", "Numerical", "mcq",
"100 students appeared in two exams. 60 passed the first, 50 passed the second and 30 passed both. Probability that a randomly selected student failed in both exams is:",
"5/6", "1/5", "1/7", "5/7",
"1", 2),

("TCS", "Numerical", "mcq",
"There are 10 points on line AB and 8 points on line AC, none being A. Number of triangles that can be formed is:",
"680", "720", "816", "640",
"3", 3),

("TCS", "Numerical", "mcq",
"From a bag containing 8 green and 5 red balls, the probability of drawing 3 green balls successively with replacement is:",
"512/2197", "336/1716", "512/1716", "336/2197",
"0", 2),

("TCS", "Numerical", "mcq",
"Find the greatest number that divides 148, 246 and 623 leaving remainders 4, 6 and 11 respectively.",
"20", "12", "6", "48",
"1", 2),

("TCS", "Numerical", "mcq",
"Mother, daughter and infant together weigh 74 kg. Mother weighs 46 kg more than daughter and infant together. Infant weighs 60% less than daughter. Daughter weighs:",
"9 kg", "11 kg", "10 kg", "12 kg",
"2", 3),

("TCS", "Numerical", "mcq",
"In how many ways can a batsman score exactly 200 runs using only boundaries of 4 and 6?",
"15", "16", "17", "18",
"1", 3),

("TCS", "Numerical", "mcq",
"Thomas paints a house in 7 days and Raj paints the same in 9 days. Working together, they can complete it in approximately:",
"4 days", "2 days", "5 days", "3 days",
"0", 1),

("TCS", "Numerical", "mcq",
"How many positive integers less than 4300 can be formed using the digits 0,1,2,3,4?",
"560", "565", "575", "625",
"2", 3),

("TCS", "Numerical", "mcq",
"A cyclist moves at 7.5 kmph and a train at 30 kmph over the same distance. The train reaches 30 minutes earlier. Find the distance.",
"5 km", "10 km", "15 km", "20 km",
"0", 2),

("TCS", "Numerical", "mcq",
"One bag contains 8 white and 3 blue balls, another contains 7 white and 4 blue balls. A bag is selected at random and one ball is drawn. Probability that it is blue is:",
"3/7", "7/22", "7/25", "7/15",
"1", 2),

("TCS", "Numerical", "mcq",
"In a 3×3 grid each tile is painted either red or blue. If after 180° rotation the grid looks the same, total possible colorings are:",
"16", "32", "64", "256",
"1", 3),

("TCS", "Numerical", "mcq",
"Jake digs a well in 16 days, Paul in 24 days, and together with Hari they finish in 8 days. Hari alone can dig the well in:",
"48 days", "96 days", "24 days", "32 days",
"0", 2),

("TCS", "Numerical", "mcq",
"On throwing two dice, the probability of getting a sum of 5 before getting a sum of 7 is:",
"40%", "45%", "50%", "60%",
"0", 2),

("TCS", "Numerical", "mcq",
"How many liters of 90% acid must be mixed with 75% acid solution to get 30 liters of 78% acid solution?",
"8", "9", "7", "6",
"3", 2),

("TCS", "Numerical", "mcq",
"Average of A, B and C is 48. With D included average becomes 47. E is 3 more than D. Average of B, C, D and E is 48. Find A.",
"42", "43", "53", "56",
"1", 3),

("TCS", "Numerical", "mcq",
"Rejection rates are 4% and 8% for two car models. Combined rejection rate is 7%. Production ratio of first to second model is:",
"3:1", "2:1", "1:1", "1:3",
"3", 3),

("TCS", "Numerical", "mcq",
"If A = x^3y^2 and B = xy^3, then the HCF of A and B is:",
"x^4y^5", "xy^2", "xy", "x^3",
"1", 1),

("TCS", "Numerical", "mcq",
"A does 1/4 of work in 2 days, B does 2/3 of work in 4 days, and all three together complete the work in 3 days. C does in one day:",
"1/12", "1/8", "1/16", "1/20",
"0", 3),

("TCS", "Numerical", "mcq",
"In how many ways can a team of 11 be selected from 5 men and 11 women such that not more than 3 men are selected?",
"1565", "2256", "2456", "1243",
"1", 3),

("TCS", "Numerical", "mcq",
"When three dice are rolled together, probability that the sum is 13 is:",
"19/216", "21/216", "17/216", "23/216",
"1", 2),

("TCS", "Numerical", "mcq",
"A 26-question test awards +8 for every correct answer and -5 for every wrong answer. If total score is zero, number of correct answers is:",
"10", "11", "12", "13",
"0", 2),

("TCS", "Numerical", "mcq",
"Two alloys are mixed in ratio 4:3 where their metal compositions are 5:3 and 1:2. The resulting ratio of metals is:",
"1:1", "2:3", "5:2", "4:3",
"0", 3),

("TCS", "Numerical", "mcq",
"M is 30% of Q, Q is 20% of P, and N is 50% of P. Then M/N =",
"4/3", "3/25", "6/5", "3/250",
"1", 2),

("TCS", "Numerical", "mcq",
"Three circles with radii 3 cm, 4 cm and 5 cm touch each other externally. Find the area of the triangle formed by joining their centers.",
"24 sq.cm", "12 sq.cm", "18 sq.cm", "30 sq.cm",
"0", 3),

("TCS", "Numerical", "mcq",
"A and B start a business investing ₹24000 and ₹36000 respectively. After 4 months, A doubles his investment. Find their profit sharing ratio at the end of the year.",
"4:7", "5:8", "3:5", "7:10",
"0", 3),

("TCS", "Numerical", "mcq",
"If the sum of first n natural numbers is 210, then value of n is:",
"20", "21", "19", "18",
"1", 2),

("TCS", "Numerical", "mcq",
"A shopkeeper sells two articles for ₹990 each. On one he gains 10% and on the other he loses 10%. Overall result is:",
"No profit no loss", "1% loss", "1% gain", "2% loss",
"1", 2),

("TCS", "Numerical", "mcq",
"The ratio of incomes of A and B is 3:4 and their expenditures are in ratio 2:3. If both save ₹6000, income of B is:",
"₹18000", "₹20000", "₹24000", "₹30000",
"2", 3),

("TCS", "Numerical", "mcq",
"A train 150 m long crosses another train 100 m long moving in opposite direction in 10 seconds. If their speeds differ by 18 kmph, find faster train speed.",
"54 kmph", "60 kmph", "72 kmph", "90 kmph",
"1", 3),

("TCS", "Numerical", "mcq",
"The average of 11 numbers is 50. If the average of first 6 is 49 and last 6 is 52, the middle number is:",
"45", "47", "49", "51",
"0", 3),

("TCS", "Numerical", "mcq",
"If a number is increased by 20% and then decreased by 20%, net percentage change is:",
"0%", "4% decrease", "4% increase", "2% decrease",
"1", 1),

("TCS", "Numerical", "mcq",
"A vessel contains milk and water in ratio 7:3. 20 liters mixture is removed and replaced with water. Final ratio becomes 5:3. Original quantity was:",
"70 liters", "80 liters", "90 liters", "100 liters",
"1", 3),

("TCS", "Numerical", "mcq",
"Find the number of zeros at the end of 100!.",
"22", "24", "25", "26",
"1", 2),

("TCS", "Numerical", "mcq",
"If 15 men can complete a work in 24 days, then 18 women can complete same work in 20 days. In how many days can 9 men and 9 women complete it?",
"20", "22", "24", "26",
"2", 3),

("TCS", "Numerical", "mcq",
"A sum doubles itself in 8 years at simple interest. In how many years will it become four times?",
"16", "20", "24", "32",
"2", 2),

("TCS", "Numerical", "mcq",
"How many numbers between 100 and 1000 are divisible by both 5 and 7?",
"24", "25", "26", "27",
"2", 2),

("TCS", "Numerical", "mcq",
"A person buys 12 pens for ₹120 and sells them at 20% profit per pen. Selling price of each pen is:",
"₹11", "₹12", "₹13", "₹14",
"1", 1),

("TCS", "Numerical", "mcq",
"If tan θ = 3/4, then sec θ = ?",
"5/4", "4/5", "3/5", "5/3",
"0", 2),

("TCS", "Numerical", "mcq",
"A man sells an article at 20% profit. Had he bought it at 10% less and sold it for ₹60 less, he would have gained 25%. Cost price is:",
"₹400", "₹480", "₹500", "₹600",
"1", 3),

("TCS", "Numerical", "mcq",
"The average of 15 numbers is 28. If each number is increased by 4, the new average becomes:",
"30", "31", "32", "33",
"2", 1),

("TCS", "Numerical", "mcq",
"A and B together can do a work in 12 days, B and C in 15 days, A and C in 20 days. In how many days can A, B and C together complete the work?",
"10", "12", "8", "9",
"0", 3),

("TCS", "Numerical", "mcq",
"A sum of money becomes ₹1331 in 3 years at 10% compound interest. Principal is:",
"₹900", "₹1000", "₹1100", "₹1200",
"1", 2),

("TCS", "Numerical", "mcq",
"The ratio of present ages of father and son is 7:3. After 10 years it becomes 9:5. Father's present age is:",
"35", "42", "49", "56",
"1", 3),

("TCS", "Numerical", "mcq",
"How many numbers between 1 and 500 are divisible by 3 or 5?",
"233", "234", "235", "236",
"0", 3),

("TCS", "Numerical", "mcq",
"If the selling price of 12 articles equals the cost price of 15 articles, profit percentage is:",
"20%", "25%", "22%", "18%",
"1", 2),

("TCS", "Numerical", "mcq",
"A train running at 54 kmph crosses a man running at 9 kmph in opposite direction in 12 seconds. Length of train is:",
"180 m", "210 m", "240 m", "250 m",
"1", 2),

("TCS", "Numerical", "mcq",
"The HCF of two numbers is 12 and their LCM is 720. If one number is 144, the other is:",
"48", "60", "72", "80",
"1", 2),

("TCS", "Numerical", "mcq",
"A shopkeeper gains 15% after giving 10% discount. Marked price is what percent above cost price?",
"25%", "27.5%", "30%", "32%",
"1", 3),

("TCS", "Numerical", "mcq",
"If 8 men can do a work in 15 days, 12 women can do it in 20 days. In how many days can 4 men and 6 women do it?",
"20", "25", "30", "35",
"2", 3),

("TCS", "Numerical", "mcq",
"How many terms are there in AP: 7, 11, 15, ... , 99?",
"22", "23", "24", "25",
"1", 2),

("TCS", "Numerical", "mcq",
"A person spends 30% of income on rent and 20% of remaining on food. If he saves ₹5600, income is:",
"₹10000", "₹12000", "₹14000", "₹15000",
"0", 2),

("TCS", "Numerical", "mcq",
"Find the least number which when divided by 12, 18 and 24 leaves remainder 5 in each case.",
"67", "71", "75", "77",
"3", 3),

("TCS", "Numerical", "mcq",
"If cos θ = 12/13, then tan θ = ?",
"5/12", "12/5", "13/5", "5/13",
"0", 2),

("TCS", "Numerical", "mcq",
"A man can row 18 km downstream in 3 hours and the same distance upstream in 6 hours. Speed of the stream is:",
"1.5 kmph", "2 kmph", "3 kmph", "4.5 kmph",
"1", 2),

("TCS", "Numerical", "mcq",
"A dishonest dealer marks his goods 20% above cost price and uses a weight 10% less. His total gain percentage is:",
"30%", "32%", "33⅓%", "35%",
"2", 3),

("TCS", "Numerical", "mcq",
"The average marks of 30 students is 52. If the marks of teacher are included, average becomes 53. Teacher's marks are:",
"81", "82", "83", "84",
"2", 2),

("TCS", "Numerical", "mcq",
"If a number when divided by 13 leaves remainder 5, what remainder will its square leave when divided by 13?",
"10", "11", "12", "9",
"3", 3),

("TCS", "Numerical", "mcq",
"A and B can do a piece of work in 10 days, B and C in 12 days, A and C in 15 days. All three together can do it in:",
"8 days", "9 days", "7 days", "6 days",
"0", 3),

("TCS", "Numerical", "mcq",
"Two pipes fill a tank in 20 min and 30 min respectively while a leak empties it in 60 min. Time to fill the tank when all are opened is:",
"10 min", "12 min", "15 min", "18 min",
"2", 2),

("TCS", "Numerical", "mcq",
"If 20% of A = 30% of B and B = ₹600, then A =",
"₹800", "₹850", "₹900", "₹950",
"2", 2),

("TCS", "Numerical", "mcq",
"A person buys an article for ₹800 and sells at 15% profit. If he had sold for ₹92 more, profit percent would be:",
"25%", "26.5%", "27%", "28%",
"1", 3),

("TCS", "Numerical", "mcq",
"The least perfect square divisible by 18, 24 and 30 is:",
"3600", "7200", "900", "1800",
"0", 3),

("TCS", "Numerical", "mcq",
"The ratio of two numbers is 5:7 and their LCM is 210. The numbers are:",
"30,42", "35,49", "25,35", "15,21",
"0", 2),

("TCS", "Numerical", "mcq",
"A sum invested at compound interest becomes 1.21 times in 2 years. Annual rate of interest is:",
"9%", "10%", "11%", "12%",
"1", 2),

("TCS", "Numerical", "mcq",
"How many numbers between 1000 and 2000 are divisible by 13?",
"76", "77", "78", "79",
"1", 2),

("TCS", "Numerical", "mcq",
"The selling price of 8 articles equals the cost price of 10 articles. Profit percent is:",
"20%", "22%", "25%", "28%",
"2", 2),

("TCS", "Numerical", "mcq",
"If sin θ = 5/13, then cos θ = ?",
"12/13", "13/12", "5/12", "12/5",
"0", 2),

("TCS", "Numerical", "mcq",
"The sum of first 20 odd natural numbers is:",
"380", "390", "400", "420",
"2", 1),

# ---------------- VERBAL ----------------
("TCS", "Verbal", "mcq",
"Choose correct sentence:",
"He has went to school", "He has gone to school", "He gone school", "He going school",
"1", 1),

("TCS", "Verbal", "mcq",
"Synonym of 'Meticulous'",
"Careless", "Precise", "Lazy", "Angry",
"1", 1),

("TCS", "Verbal", "mcq",
"Antonym of 'Scarcity'",
"Lack", "Abundance", "Shortage", "Rare",
"1", 1),

("TCS", "Verbal", "mcq",
"Fill the blank: She insisted ___ going.",
"for", "on", "to", "with",
"1", 1),

("TCS", "Verbal", "mcq",
"Meaning of idiom 'Break the ice'",
"Start conversation", "Break object", "Destroy relation", "Anger someone",
"0", 1),

("TCS", "Verbal", "mcq",
"Choose correct spelling:",
"Accomodate", "Acommodate", "Accommodate", "Acomodate",
"2", 1),

("TCS", "Verbal", "mcq",
"Choose the word nearest in meaning to 'ABATE'.",
"Increase", "Lessen", "Support", "Delay",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose the word opposite in meaning to 'VIVID'.",
"Bright", "Dull", "Clear", "Sharp",
"1", 1),

("TCS", "Verbal", "mcq",
"Select the correctly spelled word.",
"Accomodate", "Acommodate", "Accommodate", "Acomodate",
"2", 1),

("TCS", "Verbal", "mcq",
"Choose the correct synonym for 'CANDID'.",
"Honest", "Hidden", "Rough", "Cruel",
"0", 1),

("TCS", "Verbal", "mcq",
"Choose the correct antonym for 'SCARCE'.",
"Rare", "Plenty", "Thin", "Small",
"1", 1),

("TCS", "Verbal", "mcq",
"Fill in the blank: She has been working here _____ 2018.",
"for", "since", "from", "at",
"1", 1),

("TCS", "Verbal", "mcq",
"Fill in the blank: Neither the manager nor the employees _____ willing to compromise.",
"is", "are", "was", "be",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose the grammatically correct sentence.",
"He do not like coffee.", "He does not likes coffee.", "He does not like coffee.", "He not like coffee.",
"2", 1),

("TCS", "Verbal", "mcq",
"Choose the part of the sentence with an error: 'Each of the players have received a medal.'",
"Each of", "the players", "have received", "a medal",
"2", 2),

("TCS", "Verbal", "mcq",
"Choose the correct passive voice of: 'They completed the project on time.'",
"The project completed on time.", "The project was completed on time.", "The project is completed on time.", "The project has completed on time.",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose the correct indirect speech: He said, 'I am tired.'",
"He said that he is tired.", "He said that I was tired.", "He said that he was tired.", "He says that he was tired.",
"2", 2),

("TCS", "Verbal", "mcq",
"Select the appropriate word: The CEO addressed the employees in a very _____ tone.",
"authoritative", "authority", "author", "authorize",
"0", 2),

("TCS", "Verbal", "mcq",
"Choose the correct one-word substitution for 'A person who loves books'.",
"Bibliophile", "Philanthropist", "Linguist", "Orator",
"0", 1),

("TCS", "Verbal", "mcq",
"Choose the correct idiom meaning: 'Break the ice'.",
"To crack something", "To begin a conversation", "To end friendship", "To feel cold",
"1", 1),

("TCS", "Verbal", "mcq",
"Choose the correct meaning of idiom: 'Hit the nail on the head'.",
"To hit strongly", "To be exactly right", "To hurt someone", "To miss a point",
"1", 1),

("TCS", "Verbal", "mcq",
"Rearrange the sentence parts to form a meaningful sentence: P. in the park Q. children were playing R. happily S. yesterday",
"QSPR", "SQPR", "QSRP", "SPQR",
"2", 2),

("TCS", "Verbal", "mcq",
"Choose the correct article: He is _____ honest man.",
"a", "an", "the", "no article",
"1", 1),

("TCS", "Verbal", "mcq",
"Fill in the blank: If I _____ rich, I would travel the world.",
"am", "was", "were", "be",
"2", 2),

("TCS", "Verbal", "mcq",
"Choose the sentence with correct punctuation.",
"However I decided to stay.", "However, I decided to stay.", "However I, decided to stay.", "However; I decided to stay",
"1", 1),

("TCS", "Verbal", "mcq",
"Choose the synonym of 'METICULOUS'.",
"Careless", "Detailed", "Angry", "Simple",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose the antonym of 'TRANSPARENT'.",
"Visible", "Opaque", "Clear", "Open",
"1", 1),

("TCS", "Verbal", "mcq",
"Select the correctly spelled word.",
"Questionnaire", "Questionare", "Quesionnaire", "Questionnair",
"0", 1),

("TCS", "Verbal", "mcq",
"Choose the correct phrasal verb meaning: 'Look after'.",
"Search for", "Take care of", "Look behind", "Inspect",
"1", 1),

("TCS", "Verbal", "mcq",
"Choose the correct sentence transformation: 'No other city is as large as Mumbai.'",
"Mumbai is larger than all cities.", "Mumbai is the largest city.", "Mumbai is larger city.", "Mumbai largest city.",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose the word nearest in meaning to 'RELUCTANT'.",
"Willing", "Unwilling", "Ready", "Fast",
"1", 1),

("TCS", "Verbal", "mcq",
"Choose the antonym of 'OPTIMISTIC'.",
"Positive", "Hopeful", "Pessimistic", "Cheerful",
"2", 1),

("TCS", "Verbal", "mcq",
"Fill in the blank: The report must be submitted _____ Monday.",
"at", "by", "on", "from",
"1", 1),

("TCS", "Verbal", "mcq",
"Choose the grammatically correct sentence.",
"She enjoys to dance.", "She enjoys dancing.", "She enjoy dancing.", "She enjoying dance.",
"1", 1),

("TCS", "Verbal", "mcq",
"Find the error: 'One of my friend live in Delhi.'",
"One of", "my friend", "live", "in Delhi",
"2", 2),

("TCS", "Verbal", "mcq",
"Choose the passive voice: 'Someone stole my bike.'",
"My bike stole.", "My bike was stolen.", "My bike is stolen.", "My bike stolen.",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose the indirect speech: She said, 'I will call you.'",
"She said that she will call me.", "She said that she would call me.", "She says she would call me.", "She said that I would call her.",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose one-word substitution for 'A speech delivered without preparation'.",
"Lecture", "Debate", "Extempore", "Monologue",
"2", 2),

("TCS", "Verbal", "mcq",
"Meaning of idiom 'Once in a blue moon'.",
"Very frequently", "Rarely", "At night", "Never",
"1", 1),

("TCS", "Verbal", "mcq",
"Meaning of idiom 'Spill the beans'.",
"Cook food", "Reveal a secret", "Waste time", "Talk nonsense",
"1", 1),

("TCS", "Verbal", "mcq",
"Arrange in proper order: P. was raining Q. heavily R. it S. yesterday",
"RPQS", "SRPQ", "RPSQ", "SQRP",
"0", 2),

("TCS", "Verbal", "mcq",
"Choose the correct article: She bought _____ umbrella.",
"a", "an", "the", "no article",
"1", 1),

("TCS", "Verbal", "mcq",
"Fill in the blank: Had I known, I _____ helped you.",
"will have", "would have", "would", "had",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose the correctly punctuated sentence.",
"Lets eat Grandma.", "Let's eat, Grandma.", "Lets eat, Grandma.", "Let's eat Grandma.",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose synonym of 'DILIGENT'.",
"Lazy", "Hardworking", "Rude", "Weak",
"1", 1),

("TCS", "Verbal", "mcq",
"Choose antonym of 'BENEVOLENT'.",
"Kind", "Cruel", "Helpful", "Gentle",
"1", 2),

("TCS", "Verbal", "mcq",
"Select correctly spelled word.",
"Entrepreneur", "Entreprenuer", "Enterpreneur", "Entreprenaur",
"0", 2),

("TCS", "Verbal", "mcq",
"Meaning of phrasal verb 'Give up'.",
"Offer", "Surrender", "Donate", "Push",
"1", 1),

("TCS", "Verbal", "mcq",
"Choose correct transformation: 'Very few metals are as costly as gold.'",
"Gold is the costliest metal.", "Gold is one of the costliest metals.", "Gold is costlier than all metals.", "Gold costly metal.",
"1", 2),

("TCS", "Verbal", "mcq",
"Choose synonym of 'FRAGILE'.",
"Strong", "Delicate", "Hard", "Huge",
"1", 1),

("TCS", "Verbal", "mcq",
"Choose antonym of 'ANCIENT'.",
"Old", "Modern", "Historic", "Aged",
"1", 1),

("TCS", "Verbal", "mcq",
"Fill in the blank: He insisted _____ paying the bill.",
"on", "for", "at", "to",
"0", 2),

("TCS", "Verbal", "mcq",
"Choose grammatically correct sentence.",
"Neither of the boys were absent.", "Neither of the boys was absent.", "Neither boys was absent.", "Neither boy were absent.",
"1", 2),

("TCS", "Verbal", "mcq",
"Find the error: 'She has wrote a letter.'",
"She", "has", "wrote", "a letter",
"2", 1),

("TCS", "Verbal", "mcq",
"Choose one-word substitution for 'A place where books are kept'.",
"Laboratory", "Library", "Museum", "Gallery",
"1", 1),

("TCS", "Verbal", "mcq",
"Meaning of idiom 'Under the weather'.",
"Outside", "Sick", "Happy", "Busy",
"1", 1),

# ---------------- REASONING ----------------
("TCS", "Reasoning", "mcq",
"Find next number: 2, 6, 12, 20, 30, ?",
"36", "40", "42", "44",
"2", 1),

("TCS", "Reasoning", "mcq",
"If A=1, B=2,... find value of DOG.",
"26", "27", "28", "29",
"0", 1),

("TCS", "Reasoning", "mcq",
"Odd one out: Cow, Dog, Tiger, Car",
"Cow", "Dog", "Tiger", "Car",
"3", 1),

("TCS", "Reasoning", "mcq",
"Find missing number: 3, 9, 27, ?, 243",
"54", "81", "72", "90",
"1", 1),

("TCS", "Reasoning", "mcq",
"If South-East becomes North, what will West become?",
"South", "North-East", "East", "North-West",
"0", 1),

("TCS", "Reasoning", "mcq",
"Mirror image of 2:30 will be?",
"9:30", "8:30", "10:30", "7:30",
"0", 1),

("TCS", "Reasoning", "mcq",
"1,2,2,3,3,3,4,4,4,4,... Which number appears at the 2320th position?",
"2", "1", "3", "4",
"1", 3),

("TCS", "Reasoning", "mcq",
"If March 11, 2003 was Tuesday, then March 11, 2004 was:",
"Wednesday", "Tuesday", "Thursday", "Monday",
"2", 2),

("TCS", "Reasoning", "mcq",
"How many 6-digit even numbers can be formed from digits 1 to 7 without repetition such that the second last digit is even?",
"6480", "320", "2160", "720",
"3", 3),

("TCS", "Reasoning", "mcq",
"5 letters are placed randomly into 5 addressed envelopes. Total derangements possible are:",
"119", "44", "53", "40",
"1", 3),

("TCS", "Reasoning", "mcq",
"The minute hand is 8 cm and hour hand is 7 cm. Total distance covered by both tips in 4 days is:",
"1824π", "1648π", "1724π", "2028π",
"1", 3),

("TCS", "Reasoning", "mcq",
"20 persons sit in a circle with 18 men and 2 sisters such that sisters are separated by exactly one man. Number of arrangements is:",
"18!×2", "17!", "17!×2", "12",
"0", 3),

("TCS", "Reasoning", "mcq",
"Letters in PLACES are arranged alphabetically. The 48th word formed is:",
"AESPCL", "ALCEPS", "ALSCEP", "AESPLC",
"3", 3),

("TCS", "Reasoning", "mcq",
"A child can climb 10 stairs taking either 1 or 2 steps at a time. Number of distinct ways is:",
"10", "21", "89", "36",
"2", 2),

("TCS", "Reasoning", "mcq",
"Find the 32nd word formed by permuting the letters of MONOS in alphabetical order.",
"OSMON", "OSNOM", "OSMNO", "ONMSO",
"3", 3),

("TCS", "Reasoning", "mcq",
"Complete the series: 4, 20, 35, 49, 62, 74, ?",
"76", "79", "78", "85",
"3", 1),

("TCS", "Reasoning", "mcq",
"One digit is hidden. Statements: digit is 1, digit is not 2, digit is not 9, digit is 8. Three are true and one false. Which statement is definitely true?",
"Digit is 1", "Digit is not 2", "Digit is not 9", "Digit is 8",
"2", 3),

("TCS", "Reasoning", "mcq",
"Tickets are numbered from 1 to 1100. Probability that a randomly selected ticket contains the digit 2 is:",
"29/110", "32/110", "30/110", "22/110",
"0", 3),

("TCS", "Reasoning", "mcq",
"How many times does digit 2 occur between 112 and 375?",
"313", "159", "156", "315",
"2", 2),

("TCS", "Reasoning", "mcq",
"Sequence 0,2,2,4,... where each term is the unit digit of sum of previous two terms. Smallest n such that sum exceeds 2771 is:",
"692", "693", "694", "700",
"1", 3),

("TCS", "Reasoning", "mcq",
"A cube is painted on all faces and cut into 64 smaller equal cubes. Number of cubes with exactly two painted faces is:",
"24", "16", "32", "8",
"0", 3),

("TCS", "Reasoning", "mcq",
"In a certain code, COMPUTER is written as RFUVQNPC. How is MEDICINE written?",
"FOJDJEFN", "ENICIDEM", "MFEDJJOE", "ENJDJEFN",
"0", 3),

("TCS", "Reasoning", "mcq",
"If SOUTH is coded as PTVUI, then NORTH is coded as:",
"OPSUI", "OPSVH", "OPSUJ", "OPSVI",
"0", 2),

("TCS", "Reasoning", "mcq",
"A is taller than B, C is taller than A, D is shorter than B. Who is the tallest?",
"A", "B", "C", "D",
"2", 1),

("TCS", "Reasoning", "mcq",
"Statements: Some cats are dogs. All dogs are animals. Conclusion: Some cats are animals.",
"Definitely true", "Definitely false", "Cannot be determined", "None",
"0", 2),

("TCS", "Reasoning", "mcq",
"Find the missing term: AZ, BY, CX, DW, ?",
"EV", "FU", "GU", "EW",
"0", 2),

("TCS", "Reasoning", "mcq",
"If today is Wednesday, what day will it be after 100 days?",
"Thursday", "Friday", "Saturday", "Sunday",
"1", 2),

("TCS", "Reasoning", "mcq",
"A clock shows 3:15. Angle between hour and minute hand is:",
"0°", "7.5°", "15°", "22.5°",
"1", 2),

("TCS", "Reasoning", "mcq",
"Pointing to a woman, Ravi says 'She is the daughter of my grandfather's only son.' How is the woman related to Ravi?",
"Sister", "Cousin", "Mother", "Aunt",
"0", 2),

("TCS", "Reasoning", "mcq",
"How many meaningful English words can be formed with letters AER using each letter once?",
"1", "2", "3", "4",
"1", 1),

("TCS", "Reasoning", "mcq",
"If all pencils are pens and all pens are books, then all pencils are books is:",
"True", "False", "Cannot say", "None",
"0", 1),

("TCS", "Reasoning", "mcq",
"In a row of 40 students, Raj is 12th from left and Aman is 15th from right. If they interchange, Raj becomes 20th from left. Position of Aman from right is:",
"23", "21", "20", "19",
"2", 3),

("TCS", "Reasoning", "mcq",
"Choose the odd pair: 2:8, 3:27, 4:64, 5:100",
"2:8", "3:27", "4:64", "5:100",
"3", 2),

("TCS", "Reasoning", "mcq",
"If DELHI is coded as CCKGH, how is MUMBAI coded?",
"LTLAZH", "LTLAZH", "LTMZZH", "MTLAZH",
"0", 3),

("TCS", "Reasoning", "mcq",
"A series follows: 5, 11, 23, 47, ?",
"91", "95", "89", "99",
"1", 2),

("TCS", "Reasoning", "mcq",
"If MONKEY is coded as XDJMNL, then TIGER is coded as:",
"IVDFQ", "QDFHU", "QDFHS", "QDGHS",
"2", 3),

("TCS", "Reasoning", "mcq",
"Choose the missing term: BDF, FHJ, JLN, ?",
"NOP", "NPR", "MOQ", "PRT",
"1", 2),

("TCS", "Reasoning", "mcq",
"A is to the north of B, B is to the east of C, C is to the south of D. In which direction is A from D?",
"North-East", "South-East", "North-West", "South-West",
"0", 2),

("TCS", "Reasoning", "mcq",
"Pointing to a photograph, Meena says 'He is the son of my mother's only son.' How is the person related to Meena?",
"Brother", "Son", "Nephew", "Cousin",
"1", 2),

("TCS", "Reasoning", "mcq",
"If in a code language EARTH = 51264, HEART = 45126, then HATER = ?",
"42156", "45216", "45162", "42516",
"0", 3),

("TCS", "Reasoning", "mcq",
"Statements: All apples are fruits. Some fruits are mangoes. Conclusion: Some apples are mangoes.",
"Definitely true", "Definitely false", "Cannot be determined", "None",
"2", 2),

("TCS", "Reasoning", "mcq",
"Find the next number: 7, 14, 28, 56, ?",
"84", "98", "112", "120",
"2", 1),

("TCS", "Reasoning", "mcq",
"If yesterday was Friday, what day will it be 200 days from now?",
"Thursday", "Friday", "Saturday", "Sunday",
"0", 2),

("TCS", "Reasoning", "mcq",
"A clock shows 9:30. Angle between the hands is:",
"75°", "90°", "105°", "120°",
"0", 2),

("TCS", "Reasoning", "mcq",
"How many different words can be formed using all letters of TEAM?",
"24", "12", "16", "20",
"0", 1),

("TCS", "Reasoning", "mcq",
"In a class of 50 students, Riya is 18th from top and 25th from bottom. How many students are between top and bottom counted positions overlapping?",
"6", "7", "8", "9",
"1", 3),

("TCS", "Reasoning", "mcq",
"Choose odd one: 64, 125, 216, 256",
"64", "125", "216", "256",
"3", 2),

("TCS", "Reasoning", "mcq",
"If all spoons are forks and all forks are knives, then all spoons are knives is:",
"True", "False", "Cannot say", "None",
"0", 1),

("TCS", "Reasoning", "mcq",
"Find missing term: AC, FH, KM, ?",
"PQ", "PR", "OQ", "RT",
"1", 2),

("TCS", "Reasoning", "mcq",
"If WATER is coded as YCVGT, then FIRE is coded as:",
"HKTG", "HKTI", "HKTG", "HKTI",
"0", 2),

("TCS", "Reasoning", "mcq",
"If LIGHT is coded as ORJWK, then SOUND is coded as:",
"VRXQG", "VRYQG", "VRYPG", "VQXRG",
"0", 2),

("TCS", "Reasoning", "mcq",
"Find the next term: CE, GI, KM, ?",
"OQ", "PR", "OQ", "QS",
"0", 2),

("TCS", "Reasoning", "mcq",
"A is west of B, B is north of C, C is east of D. In which direction is A from D?",
"North-East", "North-West", "South-East", "South-West",
"0", 2),

("TCS", "Reasoning", "mcq",
"Pointing to a girl, Rohan said 'She is the daughter of the only son of my mother.' The girl is Rohan's:",
"Daughter", "Sister", "Niece", "Cousin",
"0", 2),

("TCS", "Reasoning", "mcq",
"If TABLE = 12345 and BLEAT = 34512, then ELBAT = ?",
"53421", "54321", "54123", "53142",
"0", 3),

("TCS", "Reasoning", "mcq",
"Statements: All cars are bikes. Some bikes are trucks. Conclusion: Some cars are trucks.",
"Definitely true", "Definitely false", "Cannot be determined", "None",
"2", 2),

("TCS", "Reasoning", "mcq",
"Find next number: 9, 18, 36, 72, ?",
"124", "136", "144", "152",
"2", 1),

("TCS", "Reasoning", "mcq",
"If today is Monday, what day will it be after 150 days?",
"Monday", "Tuesday", "Wednesday", "Thursday",
"1", 2),

("TCS", "Reasoning", "mcq",
"A clock shows 6:20. Angle between hands is:",
"50°", "60°", "70°", "80°",
"1", 2),

("TCS", "Reasoning", "mcq",
"How many words can be formed using all letters of NOTE?",
"24", "12", "16", "20",
"0", 1),

("TCS", "Reasoning", "mcq",
"In a class of 60 students, Neha is 20th from top and 25th from bottom. Number of students between both positions overlap is:",
"14", "15", "16", "17",
"1", 3),

("TCS", "Reasoning", "mcq",
"Choose odd one: 27, 64, 81, 125",
"27", "64", "81", "125",
"2", 2),

("TCS", "Reasoning", "mcq",
"If all buses are vehicles and all vehicles are machines, then all buses are machines is:",
"True", "False", "Cannot say", "None",
"0", 1),

("TCS", "Reasoning", "mcq",
"Find missing term: DG, HK, LO, ?",
"PS", "PT", "QU", "RV",
"0", 2),

("TCS", "Reasoning", "mcq",
"If CLOUD is coded as FORXG, then RAIN is coded as:",
"UDLQ", "UDMQ", "VDLQ", "VDMQ",
"0", 2),

# ---------------- ADVANCED QUANTS & REASONING ----------------
("TCS", "Advanced quants & reasoning", "mcq",
"Rice of ₹50/kg and ₹60/kg are mixed and sold at ₹70/kg with 20% profit. Ratio of quantities mixed is:",
"1:10", "3:8", "1:5", "2:7",
"2", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"If f(x)=ax^4−bx^2+x+5 and f(−3)=2, then f(3)= ?",
"3", "7", "8", "6",
"2", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Sum of 5 numbers in AP is 30 and sum of their squares is 190. Third term is:",
"5", "6", "8", "9",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Least number which when divided by 48, 60, 72, 108 and 140 leaves remainders 38, 50, 62, 98 and 130 respectively is:",
"4562", "15110", "2135", "7589",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"A sum is borrowed and repaid in two annual installments of ₹882 each at 5% compound interest. The original sum borrowed is:",
"1680", "1142", "640", "1640",
"3", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If x+y=10 and xy=21, then x²+y² = ?",
"58", "56", "52", "60",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Probability of getting exactly 2 heads when 4 coins are tossed is:",
"3/8", "1/4", "1/2", "5/8",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If x + 1/x = 5, then x² + 1/x² = ?",
"21", "23", "25", "27",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"A car covers first half of a distance at 40 kmph and the second half at 60 kmph. Average speed for whole journey is:",
"48", "50", "52", "46",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Two dice are thrown together. Probability that the product is even is:",
"1/4", "3/4", "1/2", "2/3",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If roots of equation x²−7x+10=0 are α and β, then α²+β² = ?",
"25", "29", "31", "27",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"The sum of infinite GP 8+4+2+... is:",
"8", "12", "16", "20",
"2", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If sin θ + cos θ = √2, then θ = ?",
"30°", "45°", "60°", "90°",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Probability that a leap year selected at random has 53 Sundays is:",
"1/7", "2/7", "3/7", "4/7",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"A bag has 5 white, 4 black and 3 red balls. Probability of drawing neither black nor red is:",
"5/12", "1/4", "1/3", "1/2",
"0", 1),

("TCS", "Advanced quants & reasoning", "mcq",
"If logx(81)=4, then x = ?",
"2", "3", "4", "5",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"The area bounded by x-axis and line y=2x from x=0 to x=5 is:",
"20", "25", "30", "35",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If determinant |2 3; x 5| =4, then x = ?",
"1", "2", "3", "4",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"A fair coin is tossed till a head appears. Probability that head appears on third toss is:",
"1/4", "1/8", "1/6", "3/8",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If arithmetic mean of x and y is 20 and geometric mean is 16, then x+y = ?",
"32", "36", "40", "48",
"2", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"A person covers 1/3rd journey at 30 kmph, next 1/3rd at 45 kmph and last 1/3rd at 60 kmph. Average speed is:",
"42 kmph", "43.2 kmph", "45 kmph", "46 kmph",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"If x^2 + y^2 = 25 and xy =12, then x+y = ?",
"5", "6", "7", "8",
"2", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"Find the coefficient of x² in expansion of (x+2)^4.",
"16", "24", "32", "48",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"If 3 men or 5 women can complete a work in 20 days, then 6 men and 10 women can complete it in:",
"5 days", "6 days", "8 days", "10 days",
"0", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"Probability that sum of two dice is a prime number is:",
"5/12", "1/2", "7/12", "2/3",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If matrix A=[[1,2],[3,4]], trace of A² is:",
"25", "27", "29", "30",
"2", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"If roots of x²−9x+14=0 are α and β, then α/β + β/α = ?",
"29/14", "31/14", "32/14", "27/14",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"The sum to infinity of GP 27, 9, 3, ... is:",
"36", "40.5", "42", "45",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If sec θ = 13/12, then tan θ = ?",
"5/12", "12/5", "13/5", "5/13",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Probability that in a leap year there are 53 Mondays is:",
"1/7", "2/7", "3/7", "4/7",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"A bag contains 4 red, 5 green and 3 blue balls. Probability of drawing a green ball is:",
"1/4", "5/12", "1/3", "3/4",
"1", 1),

("TCS", "Advanced quants & reasoning", "mcq",
"If logx(125)=3, then x = ?",
"3", "4", "5", "6",
"2", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Area under line y=3x from x=0 to x=4 is:",
"18", "20", "22", "24",
"3", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If determinant |3 2; x 4| =10, then x = ?",
"1", "2", "3", "4",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"A fair coin is tossed till a tail appears. Probability that tail appears on second toss is:",
"1/2", "1/4", "1/8", "3/8",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Arithmetic mean of x and y is 15 and geometric mean is 9. Then x+y = ?",
"18", "24", "30", "36",
"2", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"A man covers 1/2 journey at 20 kmph, 1/3 at 30 kmph and rest at 60 kmph. Average speed is:",
"26 kmph", "27.7 kmph", "28 kmph", "30 kmph",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"If x²+y²=41 and xy=20, then x+y = ?",
"7", "8", "9", "10",
"2", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"Coefficient of x³ in expansion of (x+1)^5 is:",
"5", "10", "15", "20",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If 4 men or 6 women can complete a work in 18 days, then 8 men and 12 women can complete it in:",
"4.5 days", "6 days", "9 days", "3 days",
"0", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"Probability that sum of two dice is divisible by 3 is:",
"1/3", "1/2", "5/12", "2/3",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If matrix A=[[2,1],[1,2]], trace of A² is:",
"8", "10", "12", "14",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"If roots of x²−11x+24=0 are α and β, then α²+β² = ?",
"71", "73", "75", "77",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"Sum to infinity of GP 16, 8, 4, ... is:",
"28", "30", "32", "34",
"2", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If cosec θ = 13/5, then cot θ = ?",
"12/5", "5/12", "13/12", "12/13",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Probability that a leap year has 53 Fridays is:",
"1/7", "2/7", "3/7", "4/7",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"A bag contains 6 red, 2 blue and 4 green balls. Probability of drawing a green ball is:",
"1/4", "1/3", "1/2", "2/3",
"1", 1),

("TCS", "Advanced quants & reasoning", "mcq",
"If logx(64)=3, then x = ?",
"3", "4", "5", "6",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Area under line y=4x from x=0 to x=3 is:",
"16", "18", "20", "24",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If determinant |4 1; x 3| =11, then x = ?",
"1", "2", "3", "4",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"A fair coin is tossed till a head appears. Probability that head appears on fourth toss is:",
"1/8", "1/16", "1/4", "3/16",
"1", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"Arithmetic mean of x and y is 18 and geometric mean is 8. Then x+y = ?",
"28", "32", "36", "40",
"2", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"A man covers 1/4 journey at 24 kmph, next 1/4 at 36 kmph and remaining at 48 kmph. Average speed is:",
"34 kmph", "35.6 kmph", "36 kmph", "37 kmph",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"If x²+y²=61 and xy=30, then x+y = ?",
"9", "10", "11", "12",
"2", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"Coefficient of x² in expansion of (x+3)^4 is:",
"36", "54", "72", "81",
"1", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"If 5 men or 10 women can complete a work in 15 days, then 10 men and 20 women can complete it in:",
"3.75 days", "4 days", "4.5 days", "5 days",
"0", 3),

("TCS", "Advanced quants & reasoning", "mcq",
"Probability that sum of two dice is even is:",
"1/2", "5/12", "2/3", "7/12",
"0", 2),

("TCS", "Advanced quants & reasoning", "mcq",
"If matrix A=[[3,1],[1,3]], trace of A² is:",
"18", "20", "22", "24",
"1", 3),

# ---------------- CODING ----------------
("TCS", "Coding", "coding",
"Given an array of integers, find the longest subarray with sum equal to zero.",
None, None, None, None, "logic", 5),

("TCS", "Coding", "coding",
"Check if a string is a valid palindrome ignoring spaces and special characters.",
None, None, None, None, "logic", 5),

("TCS", "Coding", "coding",
"Find the first non-repeating character in a string.",
None, None, None, None, "logic", 5),

("TCS", "Coding", "coding",
"Given two numbers, return indices of the two numbers such that they add up to a target.",
None, None, None, None, "logic", 5),

("TCS", "Coding", "coding",
"Given a string, find the longest substring without repeating characters.",
None, None, None, None, "logic", 5),

("TCS", "Coding", "coding",
"A railway station has N platforms represented as an array of integers where 0 indicates an empty platform and non-zero indicates a train number. The station master wants all empty platforms to be shifted to the end while maintaining the order of trains.\n\nExample 1:\nInput:\n8\n4\n5\n0\n1\n9\n0\n5\n0\nOutput:\n4 5 1 9 5 0 0 0\n\nExample 2:\nInput:\n6\n6\n0\n1\n8\n0\n2\nOutput:\n6 1 8 2 0 0",
"", "", "", "",
"move_zeroes", 2),

("TCS", "Coding", "coding",
"A bookstore contains N book IDs represented as integers. The manager wants to identify the second largest unique book ID for premium display.\n\nExample 1:\nInput:\n6\n12\n45\n67\n45\n89\n67\nOutput:\n67\n\nExample 2:\nInput:\n5\n10\n20\n30\n40\n50\nOutput:\n40",
"", "", "", "",
"second_largest", 2),

("TCS", "Coding", "coding",
"In a warehouse, N boxes are labeled with integer IDs. Some labels may repeat due to duplication. Find the first repeating label encountered in the sequence.\n\nExample 1:\nInput:\n7\n4\n5\n1\n2\n5\n7\n1\nOutput:\n5\n\nExample 2:\nInput:\n6\n9\n8\n7\n6\n8\n5\nOutput:\n8",
"", "", "", "",
"first_repeating", 2),

("TCS", "Coding", "coding",
"A smart classroom stores attendance roll numbers from 1 to N. Due to absence of one student, exactly one roll number is missing. Find the missing roll number.\n\nExample 1:\nInput:\n5\n1\n2\n3\n5\nOutput:\n4\n\nExample 2:\nInput:\n6\n1\n2\n4\n5\n6\nOutput:\n3",
"", "", "", "",
"missing_number", 1),

("TCS", "Coding", "coding",
"A digital clock factory receives a sequence of characters. The engineer wants to know whether the given sequence reads the same forward and backward.\n\nExample 1:\nInput:\nmadam\nOutput:\nPalindrome\n\nExample 2:\nInput:\nclock\nOutput:\nNot Palindrome",
"", "", "", "",
"palindrome", 1),

("TCS", "Coding", "coding",
"A delivery company records N package weights in an array. The heaviest and the lightest packages are removed before shipment. Find the sum of all remaining packages.\n\nExample 1:\nInput:\n5\n4\n8\n1\n9\n3\nOutput:\n15\n\nExample 2:\nInput:\n6\n10\n2\n7\n5\n1\n9\nOutput:\n24",
"", "", "", "",
"sum_excluding_minmax", 2),

("TCS", "Coding", "coding",
"A supermarket billing machine stores N product IDs. Count the frequency of each product ID and print them in ascending order.\n\nExample 1:\nInput:\n6\n2\n3\n2\n5\n3\n2\nOutput:\n2 -> 3\n3 -> 2\n5 -> 1\n\nExample 2:\nInput:\n5\n1\n1\n1\n4\n4\nOutput:\n1 -> 3\n4 -> 2",
"", "", "", "",
"frequency_count", 2),

("TCS", "Coding", "coding",
"A bank stores daily transaction values as positive and negative integers. Find the contiguous sequence having the maximum transaction sum.\n\nExample 1:\nInput:\n8\n-2\n-3\n4\n-1\n-2\n1\n5\n-3\nOutput:\n7\n\nExample 2:\nInput:\n5\n1\n2\n3\n4\n5\nOutput:\n15",
"", "", "", "",
"kadane", 3),

("TCS", "Coding", "coding",
"A telecom company stores customer phone numbers as strings. Find the first non-repeating digit in the string.\n\nExample 1:\nInput:\n22134514\nOutput:\n3\n\nExample 2:\nInput:\n9988776\nOutput:\n6",
"", "", "", "",
"first_non_repeating", 2),

("TCS", "Coding", "coding",
"A gaming company stores player scores in an array. Sort all the scores in ascending order without using built-in sort function.\n\nExample 1:\nInput:\n5\n9\n2\n7\n1\n5\nOutput:\n1 2 5 7 9\n\nExample 2:\nInput:\n4\n8\n3\n6\n4\nOutput:\n3 4 6 8",
"", "", "", "",
"manual_sort", 1),

("TCS", "Coding", "coding",
"A museum has N rooms represented by an array where each room contains a certain number of visitors. Find the room having maximum visitors and print its index position.\n\nExample 1:\nInput:\n5\n10\n45\n22\n67\n31\nOutput:\n3\n\nExample 2:\nInput:\n4\n99\n12\n54\n87\nOutput:\n0",
"", "", "", "",
"max_index", 1),

("TCS", "Coding", "coding",
"A school stores marks of N students in an array. Students scoring below average are selected for remedial training. Count how many students scored below average.\n\nExample 1:\nInput:\n5\n40\n60\n80\n20\n50\nOutput:\n2\n\nExample 2:\nInput:\n4\n10\n20\n30\n40\nOutput:\n2",
"", "", "", "",
"below_average", 2),

("TCS", "Coding", "coding",
"A typing machine receives a sentence. The company wants every word reversed individually while maintaining the original word order.\n\nExample 1:\nInput:\nhello world from tcs\nOutput:\nolleh dlrow morf sct\n\nExample 2:\nInput:\nsmart coding round\nOutput:\ntrams gnidoc dnuor",
"", "", "", "",
"reverse_words", 2),

("TCS", "Coding", "coding",
"A mobile company stores battery percentages of N devices. Rearrange the battery percentages such that all even values appear first followed by all odd values.\n\nExample 1:\nInput:\n6\n5\n2\n8\n1\n9\n4\nOutput:\n2 8 4 5 1 9\n\nExample 2:\nInput:\n5\n7\n6\n3\n2\n1\nOutput:\n6 2 7 3 1",
"", "", "", "",
"even_odd_rearrange", 2),

("TCS", "Coding", "coding",
"A ticket booking portal stores seat numbers from 1 to N. Due to technical issue, one seat number appears twice and one seat number is missing. Find both repeated and missing numbers.\n\nExample 1:\nInput:\n5\n1\n2\n2\n4\n5\nOutput:\nRepeated: 2 Missing: 3\n\nExample 2:\nInput:\n6\n1\n3\n4\n5\n5\n6\nOutput:\nRepeated: 5 Missing: 2",
"", "", "", "",
"repeat_missing", 3),

("TCS", "Coding", "coding",
"A weather monitoring station stores daily temperatures in an array. Find the length of the longest consecutive increasing subarray.\n\nExample 1:\nInput:\n7\n10\n12\n14\n9\n11\n13\n15\nOutput:\n4\n\nExample 2:\nInput:\n5\n5\n4\n3\n2\n1\nOutput:\n1",
"", "", "", "",
"longest_increasing", 3),

("TCS", "Coding", "coding",
"A digital wallet records daily credits and debits as integers. Find whether there exists any pair of values whose sum is zero.\n\nExample 1:\nInput:\n5\n4\n-4\n7\n2\n1\nOutput:\nYes\n\nExample 2:\nInput:\n4\n1\n2\n3\n4\nOutput:\nNo",
"", "", "", "",
"pair_sum_zero", 2),

("TCS", "Coding", "coding",
"A string encryption unit receives a word and an integer K. Shift every alphabet by K positions cyclically and print the encrypted word.\n\nExample 1:\nInput:\nabc\n2\nOutput:\ncde\n\nExample 2:\nInput:\nxyz\n3\nOutput:\nabc",
"", "", "", "",
"caesar_cipher", 2),

("TCS", "Coding", "coding",
"A chocolate company stores sweetness values of N bars in an array. Find the pair of bars whose sweetness sum is closest to a target value X.\n\nExample 1:\nInput:\n5\n2\n7\n4\n9\n1\n10\nOutput:\n1 9\n\nExample 2:\nInput:\n6\n5\n8\n12\n3\n7\n9\n15\nOutput:\n3 12",
"", "", "", "",
"closest_pair_sum", 3),

("TCS", "Coding", "coding",
"A smart city stores electricity usage of N houses. Find an equilibrium index such that left side sum equals right side sum.\n\nExample 1:\nInput:\n5\n1\n3\n5\n2\n2\nOutput:\n2\n\nExample 2:\nInput:\n4\n1\n2\n3\n4\nOutput:\n-1",
"", "", "", "",
"equilibrium_index", 3),

("TCS", "Coding", "coding",
"A toy factory stores colors of toys as integers. Find the majority color that appears more than N/2 times. If none exists print -1.\n\nExample 1:\nInput:\n7\n2\n2\n1\n2\n3\n2\n2\nOutput:\n2\n\nExample 2:\nInput:\n5\n1\n2\n3\n4\n5\nOutput:\n-1",
"", "", "", "",
"majority_element", 3),

("TCS", "Coding", "coding",
"A smart meter records N daily unit consumptions. Find the difference between maximum and minimum consumption values.\n\nExample 1:\nInput:\n5\n23\n45\n12\n67\n34\nOutput:\n55\n\nExample 2:\nInput:\n4\n9\n9\n9\n9\nOutput:\n0",
"", "", "", "",
"max_min_diff", 1),

("TCS", "Coding", "coding",
"A password system receives a string. Count the number of vowels, consonants, digits and special characters present in it.\n\nExample 1:\nInput:\nTcs@123\nOutput:\nVowels:0 Consonants:3 Digits:3 Special:1\n\nExample 2:\nInput:\nHello#9\nOutput:\nVowels:2 Consonants:3 Digits:1 Special:1",
"", "", "", "",
"char_analysis", 2),

("TCS", "Coding", "coding",
"A printing machine receives N page numbers. Find whether the page numbers form a palindrome sequence.\n\nExample 1:\nInput:\n5\n1\n2\n3\n2\n1\nOutput:\nPalindrome\n\nExample 2:\nInput:\n4\n1\n2\n3\n4\nOutput:\nNot Palindrome",
"", "", "", "",
"array_palindrome", 1),

("TCS", "Coding", "coding",
"A parking lot stores car entry times in sorted order. Find whether a given target entry time exists using efficient searching.\n\nExample 1:\nInput:\n5\n10\n20\n30\n40\n50\n30\nOutput:\nFound\n\nExample 2:\nInput:\n4\n5\n15\n25\n35\n20\nOutput:\nNot Found",
"", "", "", "",
"binary_search", 2),

("TCS", "Coding", "coding",
"A classroom stores heights of N students. Find the second shortest distinct height.\n\nExample 1:\nInput:\n5\n150\n140\n160\n140\n155\nOutput:\n150\n\nExample 2:\nInput:\n4\n170\n165\n180\n175\nOutput:\n170",
"", "", "", "",
"second_smallest", 2),

("TCS", "Coding", "coding",
"A cinema hall stores seat booking IDs in an array. Remove all duplicate IDs and print only unique IDs in original order.\n\nExample 1:\nInput:\n7\n2\n3\n2\n5\n3\n7\n8\nOutput:\n2 3 5 7 8\n\nExample 2:\nInput:\n5\n1\n1\n1\n2\n2\nOutput:\n1 2",
"", "", "", "",
"remove_duplicates", 2),

("TCS", "Coding", "coding",
"A message center receives a sentence. Print the word having maximum length.\n\nExample 1:\nInput:\nwelcome to tcs coding challenge\nOutput:\nchallenge\n\nExample 2:\nInput:\nartificial intelligence rocks\nOutput:\nintelligence",
"", "", "", "",
"longest_word", 1),

("TCS", "Coding", "coding",
"A finance office stores N transaction values. Rotate the array by K positions to the right.\n\nExample 1:\nInput:\n5\n1\n2\n3\n4\n5\n2\nOutput:\n4 5 1 2 3\n\nExample 2:\nInput:\n4\n9\n8\n7\n6\n1\nOutput:\n6 9 8 7",
"", "", "", "",
"array_rotation", 2),

("TCS", "Coding", "coding",
"A signal processing unit stores N integer amplitudes. Find the contiguous subarray having minimum sum.\n\nExample 1:\nInput:\n6\n3\n-4\n2\n-3\n-1\n7\nOutput:\n-6\n\nExample 2:\nInput:\n5\n1\n2\n3\n4\n5\nOutput:\n1",
"", "", "", "",
"min_subarray", 3),

("TCS", "Coding", "coding",
"A fruit warehouse stores N basket weights. The manager wants the baskets arranged in descending order without using any built-in sorting method.\n\nExample 1:\nInput:\n5\n12\n5\n18\n9\n2\nOutput:\n18 12 9 5 2\n\nExample 2:\nInput:\n4\n7\n1\n10\n3\nOutput:\n10 7 3 1",
"", "", "", "",
"descending_sort", 2),

("TCS", "Coding", "coding",
"A bus depot stores bus arrival numbers. Find the first bus number that appears only once in the sequence.\n\nExample 1:\nInput:\n7\n4\n5\n4\n6\n5\n7\n8\nOutput:\n6\n\nExample 2:\nInput:\n6\n9\n9\n2\n3\n2\n4\nOutput:\n3",
"", "", "", "",
"first_unique", 2),

("TCS", "Coding", "coding",
"A smart lock receives a numeric password. Determine whether the sum of digits at even positions equals the sum of digits at odd positions.\n\nExample 1:\nInput:\n1230\nOutput:\nBalanced\n\nExample 2:\nInput:\n54321\nOutput:\nNot Balanced",
"", "", "", "",
"position_digit_sum", 2),

("TCS", "Coding", "coding",
"A weather center stores rainfall data of N days. Print all days where rainfall is greater than both immediate neighboring days.\n\nExample 1:\nInput:\n6\n2\n7\n3\n8\n1\n5\nOutput:\n7 8\n\nExample 2:\nInput:\n5\n1\n4\n2\n3\n1\nOutput:\n4 3",
"", "", "", "",
"peak_elements", 3),

("TCS", "Coding", "coding",
"A message router receives a sentence. Reverse the complete sentence word order.\n\nExample 1:\nInput:\nwelcome to tcs interview\nOutput:\ninterview tcs to welcome\n\nExample 2:\nInput:\nsmart coding challenge\nOutput:\nchallenge coding smart",
"", "", "", "",
"reverse_sentence", 2),

("TCS", "Coding", "coding",
"A warehouse stores item IDs in an array. Find all pairs whose sum is exactly equal to a given target X.\n\nExample 1:\nInput:\n5\n1\n4\n5\n6\n3\n7\nOutput:\n1 6\n4 3\n\nExample 2:\nInput:\n4\n2\n8\n1\n9\n10\nOutput:\n2 8\n1 9",
"", "", "", "",
"pair_target_sum", 3),

("TCS", "Coding", "coding",
"A city parking system stores car numbers in sequence. Find the longest sequence of identical consecutive car numbers.\n\nExample 1:\nInput:\n8\n1\n1\n1\n2\n2\n3\n3\n3\nOutput:\n3\n\nExample 2:\nInput:\n6\n4\n4\n5\n5\n5\n6\nOutput:\n3",
"", "", "", "",
"longest_consecutive_same", 2),

("TCS", "Coding", "coding",
"A typing analyzer receives a string. Count how many words in the sentence start and end with the same character.\n\nExample 1:\nInput:\nlevel madam test noon\nOutput:\n3\n\nExample 2:\nInput:\napple area code data\nOutput:\n2",
"", "", "", "",
"same_start_end_words", 2),

("TCS", "Coding", "coding",
"A toy assembly line stores toy serial numbers. Find whether the serial numbers can be divided into two groups having equal sum.\n\nExample 1:\nInput:\n4\n1\n5\n5\n1\nOutput:\nYes\n\nExample 2:\nInput:\n3\n1\n2\n4\nOutput:\nNo",
"", "", "", "",
"equal_partition", 3),

("TCS", "Coding", "coding",
"A payment machine receives N transaction values. Print the cumulative running sum after each transaction.\n\nExample 1:\nInput:\n5\n2\n4\n6\n8\n10\nOutput:\n2 6 12 20 30\n\nExample 2:\nInput:\n4\n1\n1\n1\n1\nOutput:\n1 2 3 4",
"", "", "", "",
"running_sum", 1),

("TCS", "Coding", "coding",
"A security scanner receives a string containing letters and digits. Separate and print all digits first followed by all letters preserving order.\n\nExample 1:\nInput:\na1b2c3\nOutput:\n123abc\n\nExample 2:\nInput:\nx9y8z7\nOutput:\n987xyz",
"", "", "", "",
"digit_letter_separate", 2),

("TCS", "Coding", "coding",
"A robot stores movement values in an array where positive means forward and negative means backward. Find the final displacement from origin.\n\nExample 1:\nInput:\n5\n3\n-2\n4\n-1\n2\nOutput:\n6\n\nExample 2:\nInput:\n4\n-1\n-2\n3\n1\nOutput:\n1",
"", "", "", "",
"final_displacement", 1),

("TCS", "Coding", "coding",
"A digital archive stores document IDs. Find the count of IDs that are prime numbers.\n\nExample 1:\nInput:\n5\n2\n4\n5\n8\n11\nOutput:\n3\n\nExample 2:\nInput:\n4\n1\n6\n9\n10\nOutput:\n0",
"", "", "", "",
"count_primes", 2),

("TCS", "Coding", "coding",
"A signal unit receives N amplitudes. Replace every element with product of previous and next element. First and last remain unchanged.\n\nExample 1:\nInput:\n5\n2\n3\n4\n5\n6\nOutput:\n2 8 15 24 6\n\nExample 2:\nInput:\n4\n1\n2\n3\n4\nOutput:\n1 3 8 4",
"", "", "", "",
"neighbor_product", 3),

("TCS", "Coding", "coding",
"A smart classroom receives N roll numbers. Print all roll numbers that appear more than once.\n\nExample 1:\nInput:\n6\n2\n3\n2\n5\n3\n7\nOutput:\n2 3\n\nExample 2:\nInput:\n5\n1\n1\n1\n2\n2\nOutput:\n1 2",
"", "", "", "",
"duplicate_elements", 2),

("TCS", "Coding", "coding",
"A sentence formatter receives a line. Capitalize the first letter of every word.\n\nExample 1:\nInput:\nwelcome to tcs coding\nOutput:\nWelcome To Tcs Coding\n\nExample 2:\nInput:\nsmart interview round\nOutput:\nSmart Interview Round",
"", "", "", "",
"title_case", 1),

("TCS", "Coding", "coding",
"A warehouse stores N package codes. Find the median package code after sorting.\n\nExample 1:\nInput:\n5\n9\n2\n7\n1\n5\nOutput:\n5\n\nExample 2:\nInput:\n4\n8\n3\n6\n4\nOutput:\n5",
"", "", "", "",
"median_value", 2),

("TCS", "Coding", "coding",
"A navigation unit stores distances between checkpoints. Find the checkpoint from where maximum jump to next checkpoint occurs.\n\nExample 1:\nInput:\n5\n2\n5\n11\n13\n20\nOutput:\n13\n\nExample 2:\nInput:\n4\n1\n4\n10\n12\nOutput:\n4",
"", "", "", "",
"max_gap_start", 2),

("TCS", "Coding", "coding",
"A password validator receives a string. Print Valid only if it contains at least one uppercase, one lowercase, one digit and one special character.\n\nExample 1:\nInput:\nTcs@123\nOutput:\nValid\n\nExample 2:\nInput:\nhello123\nOutput:\nInvalid",
"", "", "", "",
"password_check", 2),

("TCS", "Coding", "coding",
"A drone stores altitude readings in an array. Find the longest subarray where values are strictly decreasing.\n\nExample 1:\nInput:\n7\n9\n7\n5\n6\n4\n3\n1\nOutput:\n4\n\nExample 2:\nInput:\n5\n10\n9\n8\n7\n6\nOutput:\n5",
"", "", "", "",
"longest_decreasing", 3),

]

# ✅ FINAL SAFETY CHECK (NO MORE ERRORS)
for q in questions:
    if len(q) != 10:
        print("❌ ERROR:", q)

# ✅ INSERT DATA
cursor.executemany("""
INSERT INTO mock_questions 
(company, section, q_type, question, option_a, option_b, option_c, option_d, correct_answer, points)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", questions)

conn.commit()
conn.close()

print("✅ Advanced TCS-level questions inserted successfully!")


