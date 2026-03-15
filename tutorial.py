# tutorial.py
# Comprehensive tutorial for learning logical prepositions

class LogicTutorial:
    """Comprehensive tutorial for learning logical prepositions"""
    
    @staticmethod
    def get_tutorial_content():
        return {
            'title': "📚 THE LOGIC GRIMOIRE - A BEGINNER'S GUIDE 📚",
            'introduction': """
Welcome, seeker of truth, to the Logic Grimoire! Before you embark on your journey through the 16 Gates of Truth,
you must first understand the fundamental prepositions that govern logical thought. Each preposition is like a magical
spell that transforms truth values in specific ways.

In this cathedral of logic, we study how two simple propositions (P and Q) can be combined to create new truths.
Each proposition can be either TRUE (T) or FALSE (F). When we combine them, we get 4 possible combinations:
• P=F, Q=F
• P=F, Q=T  
• P=T, Q=F
• P=T, Q=T

Let us explore each logical operation through the lens of our beloved Ave Mujica members...
""",
            'sections': [
                {
                    'title': "1️⃣ CONJUNCTION (AND) - SAKIKO'S TRUTH",
                    'symbol': '∧',
                    'character': 'Sakiko Togawa (Oblivionis)',
                    'description': """
CONJUNCTION is true ONLY when BOTH statements are true. Think of it as Sakiko's need for both memory AND oblivion
to coexist. If either part is false, the whole becomes false.

Truth Table:
P     Q     P ∧ Q
F     F       F    (Neither true → False)
F     T       F    (Only Q true → False)
T     F       F    (Only P true → False)
T     T       T    (Both true → True)

In life: "I will be happy IF AND ONLY IF I have both music AND friendship."
""",
                    'example': "Example: 'It is raining AND it is cold' is only true if both conditions are met."
                },
                {
                    'title': "2️⃣ DISJUNCTION (OR) - UIKA'S CHOICE",
                    'symbol': '∨',
                    'character': 'Uika Misumi (Doloris)',
                    'description': """
DISJUNCTION is true if AT LEAST ONE statement is true. Like Uika's world where she had either the ocean OR isolation,
but never both. The only time it's false is when both are false.

Truth Table:
P     Q     P ∨ Q
F     F       F    (Both false → False)
F     T       T    (Q true → True)
T     F       T    (P true → True)
T     T       T    (Both true → True)

In life: "I will go to the park OR stay home" - either option makes it true.
""",
                    'example': "Example: 'I will have tea OR coffee' is true if you have either (or both!)."
                },
                {
                    'title': "3️⃣ IMPLICATION (IF...THEN) - MUTSUMI'S PROMISE",
                    'symbol': '→',
                    'character': 'Mutsumi Wakaba (Mortis)',
                    'description': """
IMPLICATION is false ONLY when the first statement is true AND the second is false. Think of it as a promise:
"If P happens, THEN Q must happen." The only broken promise is when P happens but Q doesn't.

Truth Table:
P     Q     P → Q
F     F       T    (Promise not triggered → Vacuously true)
F     T       T    (Promise not triggered → Vacuously true)
T     F       F    (PROMISE BROKEN! P happened but Q didn't)
T     T       T    (Promise kept)

In life: "If you study, THEN you will pass" - only false if you study AND fail.
""",
                    'example': "Example: 'If it rains, then the ground will be wet' - only false if it rains and ground stays dry."
                },
                {
                    'title': "4️⃣ BICONDITIONAL (IF AND ONLY IF) - UMIRI'S BALANCE",
                    'symbol': '↔',
                    'character': 'Umiri Yahata (Timoris)',
                    'description': """
BICONDITIONAL is true when BOTH statements have the SAME truth value. It's like Umiri's search for balance -
either both true or both false, never mismatched.

Truth Table:
P     Q     P ↔ Q
F     F       T    (Both false → True)
F     T       F    (Different → False)
T     F       F    (Different → False)
T     T       T    (Both true → True)

In life: "You can go out IF AND ONLY IF you finish your homework" - both must align.
""",
                    'example': "Example: 'The light is on IF AND ONLY IF the switch is up' - they must match."
                },
                {
                    'title': "5️⃣ NEGATION (NOT) - NYAMU'S MASK",
                    'symbol': '¬',
                    'character': 'Nyamu Yūtenji (Amoris)',
                    'description': """
NEGATION simply reverses the truth value. Like Nyamu's masks - what appears true may be false, and vice versa.
It's the simplest but most powerful operation.

Truth Table:
P     ¬P
F      T    (False becomes True)
T      F    (True becomes False)

In life: "NOT happy" means you're unhappy. "NOT sad" means you're not sad.
""",
                    'example': "Example: If 'It is day' is true, then 'NOT day' (night) is false."
                },
                {
                    'title': "6️⃣ XOR (EXCLUSIVE OR) - UIKA'S JEALOUSY",
                    'symbol': '⊕',
                    'character': 'Uika\'s Darker Truth',
                    'description': """
XOR is true when EXACTLY ONE statement is true. Like Uika's jealousy - either Sakiko is with her OR with Mutsumi,
never both. It's exclusive.

Truth Table:
P     Q     P ⊕ Q
F     F       F    (Both false → False)
F     T       T    (Only Q true → True)
T     F       T    (Only P true → True)
T     T       F    (Both true → False)

In life: "Either you're with me OR against me" - can't be both.
""",
                    'example': "Example: 'You can have cake XOR ice cream' - choose one, not both."
                },
                {
                    'title': "7️⃣ NAND (NOT AND) - NYAMU'S VALIDATION",
                    'symbol': '↑',
                    'character': 'Nyamu\'s Digital Prison',
                    'description': """
NAND is the opposite of AND - it's false only when BOTH are true. Like Nyamu's need for validation -
she only feels 'false' (inauthentic) when she has both attention AND approval.

Truth Table:
P     Q     P ↑ Q
F     F       T    (Both false → True)
F     T       T    (Only Q true → True)
T     F       T    (Only P true → True)
T     T       F    (Both true → FALSE!)

In life: NAND is everything EXCEPT when everything is true.
""",
                    'example': "Example: 'You can't have your cake AND eat it too' - NAND of having and eating."
                },
                {
                    'title': "8️⃣ NOR (NOT OR) - UMIRI'S SAFETY",
                    'symbol': '↓',
                    'character': 'Umiri\'s Defense Mechanism',
                    'description': """
NOR is true only when BOTH are false. Like Umiri's 30-band strategy - she's safe only when she doesn't truly belong
AND they don't truly have her. It's the operation of emptiness and safety.

Truth Table:
P     Q     P ↓ Q
F     F       T    (Both false → TRUE!)
F     T       F    (Q true → False)
T     F       F    (P true → False)
T     T       F    (Both true → False)

In life: "Neither this nor that" - the only time it's true is when nothing is true.
""",
                    'example': "Example: 'I like neither tea nor coffee' - only true if you dislike both."
                }
            ],
            'tips': """
💡 PRO TIPS FOR MASTERING LOGIC:

1. MEMORIZE THE TRUTH TABLES: Each operation has a unique pattern. Practice until they become second nature.

2. USE MNEMONICS:
   • AND = Both must be True (like adding requirements)
   • OR = At least one True (like options on a menu)
   • IMPLICATION = Only broken when True → False (like a broken promise)
   • BICONDITIONAL = Both same (like matching socks)
   • XOR = Exactly one True (like a toggle switch)
   • NAND = Everything except both True (like "you can't have it all")
   • NOR = Only when both False (like "nothing is true")

3. CONNECT TO CHARACTERS: Each Ave Mujica member's struggle embodies their logical operation.
   Think of their stories when you encounter the symbols.

4. PRACTICE WITH THE GATES: The 16 Gates of Truth will test each operation randomly.
   Start with the Character Quests first - they teach through story.

5. REMEMBER: Logic isn't just abstract rules - it's how we understand choices, promises,
   relationships, and ourselves. The truth tables reflect real human dilemmas.

May the light of reason guide your path through the masquerade! 🦇
"""
        }