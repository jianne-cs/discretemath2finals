# tutorial.py
# Comprehensive tutorial for learning logical prepositions - Beginner Friendly Edition

class LogicTutorial:
    """Comprehensive tutorial for learning logical prepositions - designed for absolute beginners"""
    
    @staticmethod
    def get_tutorial_content():
        return {
            'title': "📚 THE LOGIC GRIMOIRE - A BEGINNER'S GUIDE 📚",
            'introduction': """
🌟 WELCOME, BRAVE BEGINNER! 🌟

Have you ever made a decision? Said "if this happens, then that will happen"? 
Congratulations - you've already used logic! You just didn't know it had fancy names.

WHAT IS LOGIC?
Logic is simply a way of thinking about truth and falsehood. 
Every statement in the world can be either TRUE or FALSE:
• "The sun is shining" → TRUE or FALSE
• "I am hungry" → TRUE or FALSE
• "2 + 2 = 5" → FALSE

In this grimoire, we use two basic statements called P and Q.
They can be any statements you want! Then we combine them using "logical operations"
(think of them as recipes for combining truths).

THE FOUR POSSIBLE WORLDS:
Since P can be TRUE or FALSE, and Q can be TRUE or FALSE, there are only 4 possibilities:
┌─────────┬─────────┐
│    P    │    Q    │
├─────────┼─────────┤
│  FALSE  │  FALSE  │
│  FALSE  │  TRUE   │
│  TRUE   │  FALSE  │
│  TRUE   │  TRUE   │
└─────────┴─────────┘

That's it! Just 4 combinations. Every logical operation is just a rule that tells us
whether the result is TRUE or FALSE for each of these 4 combinations.

Let's explore each operation through the stories of our Ave Mujica members...
""",
            'sections': [
                {
                    'title': "1️⃣ AND (∧) - SAKIKO'S TRUTH",
                    'symbol': '∧',
                    'character': 'Sakiko Togawa (Oblivionis)',
                    'easy_rule': 'BOTH must be true',
                    'everyday_example': '"I will be happy IF I have music AND I have friendship"',
                    'description': """
WHAT IS AND?
AND is the strict one. It only says TRUE when EVERYTHING is true.
If ANY part is false, the whole thing is false.

Think of it like:
• Making a sandwich: You need bread AND filling AND cheese. Missing any? No sandwich!
• Going to a party: You need an invitation AND transportation AND good mood. Missing one? Can't go!

TRUTH TABLE (easy memory: only row 4 is TRUE):
┌───────┬───────┬─────────┐
│   P   │   Q   │  P ∧ Q  │
├───────┼───────┼─────────┤
│ False │ False │  False  │ ← Nothing true
│ False │ True  │  False  │ ← Only Q true
│ True  │ False │  False  │ ← Only P true
│ True  │ True  │  True   │ ← BOTH true ✓
└───────┴───────┴─────────┘

SAKIKO'S STORY:
Sakiko needs both her father's well-being AND her band's success. 
If either fails, she feels her promise is broken. AND represents her struggle
to make both things true at once.
""",
                    'example': "Example: 'It is raining AND it is cold' → TRUE only if both actually happen."
                },
                {
                    'title': "2️⃣ OR (∨) - UIKA'S CHOICE",
                    'symbol': '∨',
                    'character': 'Uika Misumi (Doloris)',
                    'easy_rule': 'At least ONE must be true',
                    'everyday_example': '"I will have tea OR coffee"',
                    'description': """
WHAT IS OR?
OR is the relaxed one. It's TRUE if ANY of the statements are true.
The only time it's FALSE is when EVERYTHING is false.

Think of it like:
• Restaurant menu: You can order pizza OR pasta. Either is fine! Both is also fine!
• Weekend plans: "I'll go to the beach OR the mountains" - as long as you go somewhere, you're happy.

TRUTH TABLE (easy memory: only row 1 is FALSE):
┌───────┬───────┬─────────┐
│   P   │   Q   │  P ∨ Q  │
├───────┼───────┼─────────┤
│ False │ False │  False  │ ← Nothing true ✗
│ False │ True  │  True   │ ← Q true ✓
│ True  │ False │  True   │ ← P true ✓
│ True  │ True  │  True   │ ← Both true ✓
└───────┴───────┴─────────┘

UIKA'S STORY:
Uika grew up with only the ocean OR isolation - never both. 
OR represents her world where having just ONE thing was the only possibility.
""",
                    'example': "Example: 'I will bring an umbrella OR wear a raincoat' → True if you do at least one."
                },
                {
                    'title': "3️⃣ IF...THEN (→) - MUTSUMI'S PROMISE",
                    'symbol': '→',
                    'character': 'Mutsumi Wakaba (Mortis)',
                    'easy_rule': 'Only FALSE when TRUE → FALSE',
                    'everyday_example': '"IF you study, THEN you will pass"',
                    'description': """
WHAT IS IMPLICATION?
This one confuses everyone at first! Think of it as a PROMISE:
"If P happens, then Q MUST happen."

The ONLY broken promise is when P happens (TRUE) but Q DOESN'T happen (FALSE).
In all other cases, the promise is kept (or wasn't tested)!

Think of it like:
• Parent's promise: "If you clean your room, THEN you get ice cream"
  - You clean (TRUE), you get ice cream (TRUE) → Promise kept ✓
  - You clean (TRUE), no ice cream (FALSE) → Promise broken! ✗ (only this is false)
  - You don't clean (FALSE), you get ice cream anyway (TRUE) → Lucky you! ✓
  - You don't clean (FALSE), no ice cream (FALSE) → Expected outcome ✓

TRUTH TABLE (easy memory: only row 3 is FALSE):
┌───────┬───────┬─────────┐
│   P   │   Q   │  P → Q  │
├───────┼───────┼─────────┤
│ False │ False │  True   │ ← Promise not tested
│ False │ True  │  True   │ ← Promise not tested
│ True  │ False │  False  │ ← PROMISE BROKEN! ✗
│ True  │ True  │  True   │ ← Promise kept ✓
└───────┴───────┴─────────┘

MUTSUMI'S STORY:
Mutsumi struggles with expectations: "If I'm my mother's daughter, then I must be an actress."
She feels the weight of this implication every day.
""",
                    'example': "Example: 'If it rains, the ground gets wet' → Only false if it rains AND ground stays dry."
                },
                {
                    'title': "4️⃣ IF AND ONLY IF (↔) - UMIRI'S BALANCE",
                    'symbol': '↔',
                    'character': 'Umiri Yahata (Timoris)',
                    'easy_rule': 'Both must be the SAME',
                    'everyday_example': '"You can go out IF AND ONLY IF you finish homework"',
                    'description': """
WHAT IS BICONDITIONAL?
This is the "matchmaker" operation. It's TRUE when P and Q have the SAME truth value.
Both true together, or both false together. No mixing allowed!

Think of it like:
• Light switch: The light is on IF AND ONLY IF the switch is up
  - Switch up (TRUE), light on (TRUE) → ✓
  - Switch up (TRUE), light off (FALSE) → ✗ (broken!)
  - Switch down (FALSE), light off (FALSE) → ✓
  - Switch down (FALSE), light on (TRUE) → ✗ (impossible!)

TRUTH TABLE (easy memory: rows 1 and 4 are TRUE):
┌───────┬───────┬─────────┐
│   P   │   Q   │  P ↔ Q  │
├───────┼───────┼─────────┤
│ False │ False │  True   │ ← Both false ✓
│ False │ True  │  False  │ ← Different ✗
│ True  │ False │  False  │ ← Different ✗
│ True  │ True  │  True   │ ← Both true ✓
└───────┴───────┴─────────┘

UMIRI'S STORY:
Umiri seeks balance - either she truly belongs AND they truly want her,
or she doesn't belong AND they don't want her. Mixed situations hurt.
""",
                    'example': "Example: 'The door is open IF AND ONLY IF the key is turned' → They must match."
                },
                {
                    'title': "5️⃣ NOT (¬) - NYAMU'S MASK",
                    'symbol': '¬',
                    'character': 'Nyamu Yūtenji (Amoris)',
                    'easy_rule': 'FLIP the truth value',
                    'everyday_example': '"NOT happy" means sad',
                    'description': """
WHAT IS NEGATION?
This is the simplest - it just FLIPS the truth value.
True becomes False. False becomes True. That's it!

Think of it like:
• Light switch: NOT(light on) means light is off
• Temperature: NOT(hot) means cold
• Your mood: NOT(happy) means you're not happy (sad, angry, tired, etc.)

TRUTH TABLE (easy memory: it's the opposite):
┌───────┬─────────┐
│   P   │   ¬P    │
├───────┼─────────┤
│ False │  True   │ ← Flip!
│ True  │  False  │ ← Flip!
└───────┴─────────┘

NYAMU'S STORY:
Nyamu wears masks - what appears true (her confident persona) may be false,
and what's hidden (her true self) may be the real truth. Negation is her daily life.
""",
                    'example': "Example: If 'It is day' is TRUE, then NOT day (night) is FALSE."
                },
                {
                    'title': "6️⃣ XOR (⊕) - EXCLUSIVE CHOICE",
                    'symbol': '⊕',
                    'character': 'Uika\'s Jealousy',
                    'easy_rule': 'ONE and ONLY ONE must be true',
                    'everyday_example': '"You can have cake XOR ice cream" (choose one, not both)',
                    'description': """
WHAT IS XOR (Exclusive OR)?
XOR is like OR's strict cousin. OR is happy with both being true,
but XOR says "No! You must choose EXACTLY ONE!"

Think of it like:
• A toggle switch: You can have A OR B, but never both
• Restaurant special: "Choose soup OR salad" - you can't have both!
• Dating: "You can date me OR my friend" - picking both is not allowed

TRUTH TABLE (easy memory: rows 2 and 3 are TRUE):
┌───────┬───────┬─────────┐
│   P   │   Q   │  P ⊕ Q  │
├───────┼───────┼─────────┤
│ False │ False │  False  │ ← Nothing true ✗
│ False │ True  │  True   │ ← Only Q true ✓
│ True  │ False │  True   │ ← Only P true ✓
│ True  │ True  │  False  │ ← Both true ✗ (not allowed!)
└───────┴───────┴─────────┘

UIKA'S STORY:
Uika's jealousy says Sakiko must be with her OR with Mutsumi - never both.
XOR is the painful logic of exclusivity.
""",
                    'example': "Example: 'You can take the bus XOR the train' → You must pick one, not both."
                },
                {
                    'title': "7️⃣ NAND (↑) - NOT AND",
                    'symbol': '↑',
                    'character': 'Nyamu\'s Validation',
                    'easy_rule': 'Everything EXCEPT both true',
                    'everyday_example': '"You can\'t have your cake AND eat it too"',
                    'description': """
WHAT IS NAND?
NAND is the opposite of AND. It's FALSE only when BOTH are TRUE.
Every other combination is TRUE.

Think of it like:
• "You can't have everything" - the only time it's false is when you DO have everything
• A picky eater: "I'll eat anything EXCEPT fish AND broccoli together"

TRUTH TABLE (easy memory: only row 4 is FALSE):
┌───────┬───────┬─────────┐
│   P   │   Q   │  P ↑ Q  │
├───────┼───────┼─────────┤
│ False │ False │  True   │ ← Neither true ✓
│ False │ True  │  True   │ ← Only Q true ✓
│ True  │ False │  True   │ ← Only P true ✓
│ True  │ True  │  False  │ ← Both true ✗
└───────┴───────┴─────────┘

NYAMU'S STORY:
Nyamu only feels "false" (inauthentic) when she has both attention AND approval.
Any other combination, she's performing (being "true" to her mask).
""",
                    'example': "Example: 'You can't be rich AND healthy' (NAND) - only false if you somehow have both."
                },
                {
                    'title': "8️⃣ NOR (↓) - NOT OR",
                    'symbol': '↓',
                    'character': 'Umiri\'s Safety',
                    'easy_rule': 'ONLY when both are false',
                    'everyday_example': '"I like neither tea NOR coffee"',
                    'description': """
WHAT IS NOR?
NOR is the opposite of OR. It's TRUE only when BOTH are FALSE.
Everything else is FALSE.

Think of it like:
• "I want nothing" - the only time it's true is when you truly want nothing
• A hermit: "I see no one AND no one sees me" - that's the only time they're happy

TRUTH TABLE (easy memory: only row 1 is TRUE):
┌───────┬───────┬─────────┐
│   P   │   Q   │  P ↓ Q  │
├───────┼───────┼─────────┤
│ False │ False │  True   │ ← Both false ✓
│ False │ True  │  False  │ ← Q true ✗
│ True  │ False │  False  │ ← P true ✗
│ True  │ True  │  False  │ ← Both true ✗
└───────┴───────┴─────────┘

UMIRI'S STORY:
Umiri feels safe only when she doesn't belong AND they don't truly want her.
NOR is her defense mechanism - safety through emptiness.
""",
                    'example': "Example: 'I play in no bands' - TRUE only if you truly play in ZERO bands."
                }
            ],
            'quick_reference': """
📋 QUICK REFERENCE CARD 📋

AND (∧)  : TRUE only when BOTH are true
OR (∨)   : TRUE when at least ONE is true
NOT (¬)  : FLIPS the truth value
IMPLIES (→): FALSE only when TRUE → FALSE
IFF (↔)  : TRUE when both are the SAME
XOR (⊕)  : TRUE when EXACTLY ONE is true
NAND (↑) : FALSE only when BOTH are true
NOR (↓)  : TRUE only when BOTH are false

Memory tricks:
• AND = "All or nothing" (both needed)
• OR = "One is enough" (at least one)
• IMPLIES = "Broken promise" (only false when promise broken)
• IFF = "Mirror" (both match)
• XOR = "Choose one" (exactly one)
• NAND = "Not everything" (everything except both)
• NOR = "Nothing works" (only when nothing)
""",
            'tips': """
🎓 BEGINNER'S ROADMAP TO MASTERING LOGIC:

STEP 1: Start with the basics
  • Learn AND, OR, and NOT first - they're the foundation
  • Practice with real-life examples (not abstract letters!)
  
STEP 2: Move to IMPLICATION and IFF
  • Think of "if...then" as promises, not causes
  • Remember: IMPLICATION is ONLY false when the promise is broken

STEP 3: Tackle the tricky ones
  • XOR = "exclusive or" = one or the other, not both
  • NAND = opposite of AND
  • NOR = opposite of OR

STEP 4: Play the Character Quests!
  • Each character teaches their operation through story
  • The stories help you FEEL the logic, not just memorize it

STEP 5: Test yourself with the 16 Gates
  • Try to guess the operation before clicking
  • Pay attention to which patterns feel familiar

💡 PRO TIPS FOR BEGINNERS:

• Don't memorize - UNDERSTAND. The truth tables have patterns!
• Connect to characters: Sakiko (AND) needs both, Uika (XOR) must choose
• Use real life: "If I study, I pass" is easier to grasp than abstract P→Q
• Practice daily: Even 5 minutes helps build intuition
• It's okay to be wrong! Every mistake teaches you something

Remember: Logic isn't about being perfect - it's about understanding
how truth works. The Ave Mujica members aren't perfect either,
but they're learning, just like you.

May your journey through the masquerade illuminate your path! 🦇✨
"""
        }