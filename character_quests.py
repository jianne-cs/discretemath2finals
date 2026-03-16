# character_quests.py
# Character-specific logic quest classes with all stages using truth table puzzles

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseQuest(ABC):
    """Abstract base class for all quests"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_stage = 0
        self.completed = False
        self.stage_count = 3  # Default, override in subclasses
    
    @property
    @abstractmethod
    def quest_name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def character(self) -> str:
        pass
    
    @property
    @abstractmethod
    def role(self) -> str:
        pass
    
    @property
    @abstractmethod
    def operation(self) -> str:
        pass
    
    @property
    @abstractmethod
    def symbol(self) -> str:
        pass
    
    @abstractmethod
    def get_stage_data(self, stage: int) -> Dict[str, Any]:
        """Get data for a specific stage"""
        pass
    
    @abstractmethod
    def get_finale(self) -> Dict[str, Any]:
        """Get finale data"""
        pass
    
    def get_quest_intro(self) -> Dict[str, Any]:
        """Get quest introduction (optional override)"""
        return {
            'title': self.quest_name,
            'dialogue': f"Begin the quest for {self.character}...",
            'background': 'default'
        }


class SakikoImplicationQuest(BaseQuest):
    """Sakiko Togawa (Oblivionis) - Implication Quest"""
    
    @property
    def quest_name(self) -> str: return "The Weight of Promises"
    @property
    def character(self) -> str: return "Sakiko Togawa"
    @property
    def role(self) -> str: return "Oblivionis"
    @property
    def operation(self) -> str: return "Implication (→)"
    @property
    def symbol(self) -> str: return "→"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.stage_count = 3
    
    def get_stage_data(self, stage: int) -> Dict[str, Any]:
        stages = {
            0: {
                'title': "The Father's Debt",
                'scene': "father_apartment",
                'dialogue': """
[SCENE: Sakiko's father's rundown apartment. Empty bottles litter the floor.]

Sakiko's father: "You came... I thought you'd forgotten about me."

Sakiko: "I could never forget you, father. But Ave Mujica needs me too."

Father: "IF you truly cared about me, THEN you'd be here more often."

[Sakiko's hands tremble. She knows the logic of implication intimately -
 when P is true (she cares), Q must be true (she's here often).
 But reality isn't that simple.]

Sakiko: "Implication says that if I care, I must be here. But I DO care,
         and I CAN'T always be here. Does that make the implication false?
         Does that make ME false?"
""",
                'challenge': "Help Sakiko understand that implication isn't always about physical presence",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Cares for father', 'Q': 'Visits often', 'expected': 'T', 'lesson': 'When she cares AND visits, implication holds'},
                    {'P': 'Cares for father', 'Q': 'Rarely visits', 'expected': 'F', 'lesson': 'This is the ONLY case where implication fails'},
                    {'P': 'Does not care', 'Q': 'Visits often', 'expected': 'T', 'lesson': 'Actions can speak louder than feelings'},
                    {'P': 'Does not care', 'Q': 'Never visits', 'expected': 'T', 'lesson': 'At least there\'s no hypocrisy'}
                ],
                'lesson': "Implication only fails when the premise is true and the conclusion is false.",
                'emotional_payoff': """
Sakiko: "So... implication isn't about blame. It's about understanding
         that only one combination truly breaks a promise. Maybe I'm not
         failing as badly as I thought."
""",
                'reward': "Memory Fragment: Father's Better Days"
            },
            1: {
                'title': "The Band's Ultimatum",
                'scene': "practice_room",
                'dialogue': """
[SCENE: Ave Mujica's practice room. Tension hangs in the air.]

Nyamu: "IF you miss one more practice, THEN we'll find a new keyboardist."

[The words hang in the air like a guillotine blade.]

Sakiko: "You don't understand what I'm dealing with..."

Nyamu: "Implication doesn't care about understanding. P → Q. 
        That's the rule you taught us. You said logic is truth -
        so be truthful about your commitments."

[Sakiko realizes she's trapped by her own logic lessons.]
""",
                'challenge': "Navigate the implications of band loyalty",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Miss practice', 'Q': 'Get replaced', 'expected': 'T', 'lesson': 'If she misses AND gets replaced, the promise holds'},
                    {'P': 'Miss practice', 'Q': 'Keep position', 'expected': 'F', 'lesson': 'This breaks the implication - the only violation'},
                    {'P': 'Attend practice', 'Q': 'Get replaced', 'expected': 'T', 'lesson': 'Even if she attends, they might still replace her'},
                    {'P': 'Attend practice', 'Q': 'Keep position', 'expected': 'T', 'lesson': 'The ideal scenario'}
                ],
                'lesson': "Only one scenario breaks the promise - missing practice AND keeping position.",
                'emotional_payoff': """
Sakiko: "So even if I attend every practice, they could still replace me.
         Implication doesn't guarantee loyalty - it only exposes when promises are broken."
""",
                'reward': "Band Contract (Torn)"
            },
            2: {
                'title': "The Impossible Choice",
                'scene': "crossroads",
                'dialogue': """
[SCENE: A foggy crossroads. One path leads to the hospital, the other to the concert hall.]

Sakiko: "IF I go to father, THEN the band fails. 
         IF I go to the band, THEN father fails.
         Both P and Q cannot be true... but both implications hold.
         How can two contradictory paths both be logically valid?"

[Rain begins to fall, mixing with her tears.]

Sakiko: "Logic was supposed to give me answers. Instead, it's giving me
         two different truths. Which one is real? Which one is ME?"
""",
                'challenge': "Solve the paradox of dual implications",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Go to father', 'Q': 'Band fails', 'expected': 'T', 'lesson': 'If she goes to father, band fails - implication holds'},
                    {'P': 'Go to father', 'Q': 'Band succeeds', 'expected': 'F', 'lesson': 'This would break the implication'},
                    {'P': 'Go to band', 'Q': 'Father fails', 'expected': 'T', 'lesson': 'If she goes to band, father fails - implication holds'},
                    {'P': 'Go to band', 'Q': 'Father succeeds', 'expected': 'F', 'lesson': 'This would break the implication'}
                ],
                'lesson': "Logic doesn't make the choice for you - it only shows the consequences of each path.",
                'emotional_payoff': """
Sakiko: "I understand now. Both implications ARE true - they're just descriptions
         of different possible worlds. The choice isn't about which implication is valid;
         it's about which premise I choose to make true."
""",
                'reward': "Oblivionis' Realization"
            }
        }
        return stages.get(stage, stages[0])
    
    def get_finale(self) -> Dict[str, Any]:
        return {
            'title': "The Weight Lifted",
            'scene': "reconciliation",
            'dialogue': """
[SCENE: Months later. Sakiko sits with both her father (recovering) and her band
 (who understood and waited) in the same room. Sunlight streams through the windows.]

Sakiko: "I finally understand. Implication isn't about forcing outcomes.
         It's about being honest about what follows from our choices.
         I can care for father AND be in the band - they aren't mutually exclusive.
         Sometimes the premise changes, and that's okay."

[For the first time, she plays a melody where both hands move in harmony,
 representing the truth that both paths can coexist when implications
 are understood, not feared.]

Sakiko: "Implication taught me that truth isn't about avoiding falsehoods.
         It's about being honest about what follows from who we really are."
""",
            'reward': "Oblivionis' Gratitude + Implication Mastery",
            'unlock_song': "Gehaburn - The fire that burns away false promises"
        }


class UikaXORQuest(BaseQuest):
    """Uika Misumi (Doloris) - XOR Quest"""
    
    @property
    def quest_name(self) -> str: return "The Island of Loneliness"
    @property
    def character(self) -> str: return "Uika Misumi"
    @property
    def role(self) -> str: return "Doloris"
    @property
    def operation(self) -> str: return "XOR (⊕)"
    @property
    def symbol(self) -> str: return "⊕"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.stage_count = 4
    
    def get_stage_data(self, stage: int) -> Dict[str, Any]:
        stages = {
            0: {
                'title': "The Empty Island",
                'scene': "childhood_flashback",
                'dialogue': """
[SCENE: Young Uika on the isolated island, drawing faces in the sand.]

Young Uika: "One, two, three... I count the waves.
             If I count to one thousand, will someone appear?"

[The waves wash away her drawings.]

Young Uika: "But XOR says it's either the waves OR people.
             The ocean OR companionship. Never both.
             I either have the waves OR I have friends.
             I've never had friends, so I must have the waves.
             That's my truth."

[The isolation is palpable - every memory is either solitude OR imagination,
 but never real connection.]
""",
                'challenge': "Understand XOR in the context of absolute isolation",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Uika present', 'Q': 'Ocean present', 'expected': 'F', 'lesson': 'She can\'t be both present AND absent - XOR of existence?'},
                    {'P': 'Uika present', 'Q': 'Ocean absent', 'expected': 'T', 'lesson': 'Her alone - possible but never happened'},
                    {'P': 'Uika absent', 'Q': 'Ocean present', 'expected': 'T', 'lesson': 'Ocean alone - most common scenario'},
                    {'P': 'Uika absent', 'Q': 'Ocean absent', 'expected': 'F', 'lesson': 'Nothing exists - the void'}
                ],
                'lesson': "XOR means exactly ONE must be true - perfect for describing a world of isolation.",
                'emotional_payoff': """
Young Uika: "So my whole world has been XOR=True for as long as I can remember.
             Either I exist alone, or the ocean exists alone. We never both exist together."
""",
                'reward': "Memory: Sand Drawings"
            },
            1: {
                'title': "The First Connection",
                'scene': "sakiko_arrival",
                'dialogue': """
[SCENE: The day Sakiko arrived on the island. Young Uika hides behind a rock,
 watching this stranger who somehow found her isolated home.]

Sakiko: "Hello? Is anyone here? I got lost, and... wow, this place is beautiful!"

[Uika's heart races. Someone is here. Someone is REAL.]

Young Uika: "Sakiko came with her music and her laughter.
             Suddenly, the XOR of my world broke.
             It was no longer 'me OR the ocean' - it was 'me AND Sakiko'.
             But my heart couldn't understand AND. It only knew XOR.
             So I made a choice: Sakiko OR everything else.
             And I chose Sakiko... exclusively."

[The obsession began - a desperate attempt to maintain exclusive
 possession of the only person who ever broke through her isolation.]
""",
                'challenge': "Transition from XOR thinking to understanding AND",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Uika present', 'Q': 'Sakiko present', 'expected': 'T', 'lesson': 'XOR says true when exactly one is present'},
                    {'P': 'Uika present', 'Q': 'Sakiko absent', 'expected': 'T', 'lesson': 'Uika alone - familiar pattern'},
                    {'P': 'Uika absent', 'Q': 'Sakiko present', 'expected': 'T', 'lesson': 'Sakiko alone - new possibility'},
                    {'P': 'Uika absent', 'Q': 'Sakiko absent', 'expected': 'F', 'lesson': 'Both absent - the void returns'}
                ],
                'lesson': "XOR says 'either-or'. But love can also be AND where both are true.",
                'emotional_payoff': """
Uika: "AND means... I can exist AND Sakiko can exist, at the same time?
       We don't have to take turns being real?"
""",
                'reward': "Memory: Sakiko's First Smile"
            },
            2: {
                'title': "The Green-Eyed XOR",
                'scene': "jealousy",
                'dialogue': """
[SCENE: Uika watches Sakiko laugh with Mutsumi. Her hands clench into fists.]

Uika: "It's Sakiko OR Mutsumi. It HAS to be exclusive.
       If Sakiko chooses Mutsumi, THEN she's not choosing me.
       XOR demands exclusivity! That's the only truth I know!"

[She almost lunges at Mutsumi, stopped only by her own reflection
 in a nearby mirror - a face twisted by the very logic she couldn't escape.]

Uika: "That's... that's me? That's what XOR looks like when it's not just logic,
       when it's how you love? I look like a monster."
""",
                'challenge': "Understand how XOR creates jealousy and obsession",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Sakiko with Uika', 'Q': 'Sakiko with Mutsumi', 'expected': 'T', 'lesson': 'Uika\'s belief - exactly one should be true'},
                    {'P': 'Sakiko with Uika', 'Q': 'Sakiko not with Mutsumi', 'expected': 'T', 'lesson': 'Uika happy - her belief holds'},
                    {'P': 'Sakiko not with Uika', 'Q': 'Sakiko with Mutsumi', 'expected': 'T', 'lesson': 'Uika jealous - her belief holds but hurts'},
                    {'P': 'Sakiko not with Uika', 'Q': 'Sakiko not with Mutsumi', 'expected': 'F', 'lesson': 'Both false - emptiness'}
                ],
                'lesson': "Jealousy is XOR applied to love - but love can be AND.",
                'emotional_payoff': """
Uika: "I was going to hurt someone... because my mind couldn't accept
       that Sakiko could care for more than one person."
""",
                'reward': "Cracked Mirror Piece"
            },
            3: {
                'title': "Expanding the Heart",
                'scene': "practice_room",
                'dialogue': """
[SCENE: Uika sits alone in the practice room, playing a duet with herself.]

Uika: "A chord requires multiple notes. AND brings them together.
       XOR would say 'either C OR E OR G' - but that's not a chord.
       A chord is C AND E AND G together."

[She plays a chord - multiple notes in harmony.]

Uika: "Maybe... maybe love is like that too. Maybe I can have Sakiko
       AND have the band AND have myself, all at the same time.
       XOR for exclusive moments, AND for inclusive love."

[For the first time, she smiles - not a smile of possession, but of belonging.]
""",
                'challenge': "Practice combining AND with XOR understanding",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Exclusive moments', 'Q': 'Inclusive belonging', 'expected': 'T', 'lesson': 'Both can be true at different times'},
                    {'P': 'Exclusive moments', 'Q': 'No belonging', 'expected': 'F', 'lesson': 'Exclusive without belonging is lonely'},
                    {'P': 'No exclusive moments', 'Q': 'Inclusive belonging', 'expected': 'F', 'lesson': 'Belonging without intimacy is shallow'},
                    {'P': 'No exclusive moments', 'Q': 'No belonging', 'expected': 'F', 'lesson': 'Neither - back to isolation'}
                ],
                'lesson': "XOR and AND can coexist when applied to different aspects of a relationship.",
                'emotional_payoff': """
Uika: "I can have exclusive moments with Sakiko AND share her with others.
       The island taught me XOR, but the world needs AND."
""",
                'reward': "Doloris' First Harmony"
            }
        }
        return stages.get(stage, stages[0])
    
    def get_finale(self) -> Dict[str, Any]:
        return {
            'title': "The Island No More",
            'scene': "performance",
            'dialogue': """
[SCENE: Uika stands before the band, ready to perform. For the first time,
 she's not standing apart from them.]

Uika: "I used to think love was exclusive - XOR.
       But Ave Mujica taught me that we can all exist together - AND.
       My voice can soar alone AND blend with others.
       My heart can hold Sakiko close AND welcome you all in."

[She sings, and for the first time, her voice carries not just
 sorrow, but the joy of belonging.]

Uika: "The island is gone. The waves still crash, but now they're not
       my only companions. I have music. I have friends. I have ME.
       XOR taught me about boundaries. AND taught me about connection.
       I needed both to become whole."

[The band joins in, their harmony perfect - exclusive moments and inclusive
 love, all coexisting in the music.]
""",
            'reward': "Doloris' Liberation + XOR Mastery",
            'unlock_song': "Angles - Guardian spirits who watch over many"
        }


class MutsumiNegationQuest(BaseQuest):
    """Mutsumi Wakaba (Mortis) - Negation Quest"""
    
    @property
    def quest_name(self) -> str: return "The Face Behind the Mask"
    @property
    def character(self) -> str: return "Mutsumi Wakaba"
    @property
    def role(self) -> str: return "Mortis"
    @property
    def operation(self) -> str: return "Negation (¬)"
    @property
    def symbol(self) -> str: return "¬"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.stage_count = 4
    
    def get_stage_data(self, stage: int) -> Dict[str, Any]:
        stages = {
            0: {
                'title': "Born on Stage",
                'scene': "childhood_memory",
                'dialogue': """
[SCENE: Young Mutsumi watches her mother perform, the audience enraptured.]

Mother: "Mutsumi, you'll be a natural! You have my genes!"

[Cameras flash. Reporters swarm.]

Young Mutsumi: "But what if I'm NOT you? What if I'm just me?"

[The world expects another Minami. Every "be like your mother"
 is an erasure of herself.]

Young Mutsumi: "If I'm not my mother, then who am I? 
                 ¬Mother = ? The equation has no answer."
""",
                'challenge': "Understand identity negation",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Mutsumi = Mother', 'expected': 'F', 'lesson': 'Simple negation of identity - she is NOT her mother'},
                    {'P': 'Mutsumi = Actress', 'expected': 'F', 'lesson': 'Rejecting imposed roles - she is NOT just an actress'},
                    {'P': 'Mutsumi = Musician', 'expected': 'T', 'lesson': 'She IS a musician - this is true'},
                    {'P': 'Mutsumi = Herself', 'expected': 'T', 'lesson': 'She IS herself - the ultimate truth'}
                ],
                'lesson': "Negation of expectation creates space for true self, but also uncertainty.",
                'emotional_payoff': """
Young Mutsumi: "Every time I'm NOT my mother, I feel guilty.
                 But maybe... maybe ¬Mother doesn't mean failure.
                 Maybe it means I'm allowed to be someone else."
""",
                'reward': "Mother's Old Script (Blank Pages)"
            },
            1: {
                'title': "The Guitar's Voice",
                'scene': "crychic_days",
                'dialogue': """
[SCENE: Mutsumi holds her guitar - the one thing that's truly hers.]

Mutsumi: "With Sakiko, with CRYCHIC, I could just play.
          I was NOT an actress. I was NOT a daughter.
          I was just... Mutsumi. The negation felt like freedom."

[She strums a chord, smiling.]

Mutsumi: "When I play, I negate everything else.
          The music is my ¬world. ¬my mother. ¬my duty."

[But even in freedom, shadows lurked. The world still saw
 Minami's daughter playing pretend.]
""",
                'challenge': "Explore negation as liberation",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Is actress', 'expected': 'F', 'lesson': 'When playing, she is NOT an actress'},
                    {'P': 'Is daughter', 'expected': 'F', 'lesson': 'When playing, she is NOT just a daughter'},
                    {'P': 'Is musician', 'expected': 'T', 'lesson': 'When playing, she IS a musician'},
                    {'P': 'Is herself', 'expected': 'T', 'lesson': 'When playing, she IS herself'}
                ],
                'lesson': "Negation can create space for authentic identity, but society may not recognize it.",
                'emotional_payoff': """
Mutsumi: "When I play, I'm not anyone's daughter, not anyone's actress.
          I'm just... me. But as soon as the music stops, the negations end,
          and the expectations rush back in."
""",
                'reward': "Guitar Pick (Worn Smooth)"
            },
            2: {
                'title': "The Birth of Mortis",
                'scene': "breaking_point",
                'dialogue': """
[SCENE: The breaking point. Sakiko's harsh words echo. The pressure mounts.]

Sakiko: "You're not trying hard enough! You're just coasting on your mother's name!"

Mutsumi: "I can't... I can't be what anyone wants..."

[Something cracks. The air grows cold. A new voice emerges.]

Mortis: "She couldn't be what you wanted. So I am what she is NOT.
         I am the negation made flesh. I am everything Mutsumi cannot be.
         You want an actress? I'll give you a performance.
         You want a daughter? I'll give you obedience.
         You want anything? I'll be its opposite."

[The stage darkens as Mortis takes control - a being born entirely
 from the negation of Mutsumi's true self.]
""",
                'challenge': "Understand destructive negation",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Mutsumi present', 'Q': 'Mortis present', 'expected': 'F', 'lesson': 'They cannot both be present at once'},
                    {'P': 'Mutsumi present', 'Q': 'Mortis absent', 'expected': 'T', 'lesson': 'Mutsumi alone - vulnerable'},
                    {'P': 'Mutsumi absent', 'Q': 'Mortis present', 'expected': 'T', 'lesson': 'Mortis takes over - protective but destructive'},
                    {'P': 'Mutsumi absent', 'Q': 'Mortis absent', 'expected': 'F', 'lesson': 'Neither exists - annihilation'}
                ],
                'lesson': "When the self is constantly negated, only the negation remains.",
                'emotional_payoff': """
Mortis: "I am what happens when you negate someone too much.
         I am the shadow that grows when the light is denied.
         But even shadows... want to be real."
""",
                'reward': "Broken Mirror Shard"
            },
            3: {
                'title': "The Integration",
                'scene': "hall_of_mirrors",
                'dialogue': """
[SCENE: Mutsumi and Mortis face each other in a hall of mirrors.
 Infinite reflections stretch in all directions.]

Mutsumi: "You are me."
Mortis: "I am NOT you."
Mutsumi: "But ¬Mortis = Mutsumi."
Mortis: "And ¬Mutsumi = Mortis."

[They realize - negation creates a duality, but also a connection.
 They are two sides of the same coin, defined by each other's absence.]

Mutsumi: "We're not opposites. We're... complements."
Mortis: "Like day and night. Light and shadow. You can't have one without the other."
""",
                'challenge': "Understand that negation creates relationship, not just opposition",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Mutsumi acknowledged', 'Q': 'Mortis acknowledged', 'expected': 'T', 'lesson': 'Both acknowledged - integration'},
                    {'P': 'Mutsumi acknowledged', 'Q': 'Mortis denied', 'expected': 'F', 'lesson': 'Denying shadow leads to imbalance'},
                    {'P': 'Mutsumi denied', 'Q': 'Mortis acknowledged', 'expected': 'F', 'lesson': 'Denying self leads to loss'},
                    {'P': 'Mutsumi denied', 'Q': 'Mortis denied', 'expected': 'F', 'lesson': 'Denying both leads to nothing'}
                ],
                'lesson': "Both selves can coexist when acknowledged, not negated.",
                'emotional_payoff': """
[Mutsumi reaches out. Mortis takes her hand.]

Mutsumi: "I don't have to kill you to be me."
Mortis: "And I don't have to erase you to exist."

[They merge - not into one, but into understanding.]
""",
                'reward': "Two Halves of One Heart"
            }
        }
        return stages.get(stage, stages[0])
    
    def get_finale(self) -> Dict[str, Any]:
        return {
            'title': "Playing as One",
            'scene': "unity",
            'dialogue': """
[SCENE: Mutsumi takes the stage, guitar in hand. For the first time,
 both she and Mortis play together - two hands on one instrument,
 two souls in one body, two truths in one person.]

Mutsumi: "I am NOT just my mother's daughter."
Mortis: "I am NOT just Mutsumi's shadow."

Together: "We ARE. And that's enough."

[The music they create is unlike anything before - it contains
 both the gentle melody of Mutsumi and the powerful chords of Mortis,
 proving that negation doesn't have to mean destruction.]

Mutsumi: "Negation taught me that who I'm NOT helps define who I AM.
          Mortis taught me that even shadows have a place in the light.
          Together, we're not broken - we're complete."

[The audience doesn't see two people. They see one musician,
 whole and authentic for the first time.]
""",
            'reward': "Mortis' Integration + Negation Mastery",
            'unlock_song': "Imprisoned - Freedom found within acceptance"
        }

class MutsumiNegationQuest(BaseQuest):
    """Mutsumi Wakaba (Mortis) - Negation Quest"""
    
    @property
    def quest_name(self) -> str: return "The Face Behind the Mask"
    @property
    def character(self) -> str: return "Mutsumi Wakaba"
    @property
    def role(self) -> str: return "Mortis"
    @property
    def operation(self) -> str: return "Negation (¬)"
    @property
    def symbol(self) -> str: return "¬"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.stage_count = 4
    
    def get_stage_data(self, stage: int) -> Dict[str, Any]:
        stages = {
            0: {
                'title': "Born on Stage",
                'scene': "childhood_memory",
                'dialogue': """
[SCENE: Young Mutsumi watches her mother perform, the audience enraptured.]

Mother: "Mutsumi, you'll be a natural! You have my genes!"

[Cameras flash. Reporters swarm.]

Young Mutsumi: "But what if I'm NOT you? What if I'm just me?"

[The world expects another Minami. Every "be like your mother"
 is an erasure of herself.]

Young Mutsumi: "If I'm not my mother, then who am I? 
                 ¬Mother = ? The equation has no answer."
""",
                'challenge': "Understand identity negation",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Is her mother', 'Q': 'Is an actress', 'expected': 'F', 'lesson': 'She is NOT her mother - negation is true'},
                    {'P': 'Is her mother', 'Q': 'Is a musician', 'expected': 'F', 'lesson': 'She is NOT her mother, even as a musician'},
                    {'P': 'Is Mutsumi', 'Q': 'Is herself', 'expected': 'T', 'lesson': 'She IS Mutsumi - this is true'},
                    {'P': 'Is Mortis', 'Q': 'Is shadow', 'expected': 'F', 'lesson': 'Mortis is not yet born'}
                ],
                'lesson': "Negation of expectation creates space for true self, but also uncertainty.",
                'emotional_payoff': """
Young Mutsumi: "Every time I'm NOT my mother, I feel guilty.
                 But maybe... maybe ¬Mother doesn't mean failure.
                 Maybe it means I'm allowed to be someone else."
""",
                'reward': "Mother's Old Script (Blank Pages)"
            },
            1: {
                'title': "The Guitar's Voice",
                'scene': "crychic_days",
                'dialogue': """
[SCENE: Mutsumi holds her guitar - the one thing that's truly hers.]

Mutsumi: "With Sakiko, with CRYCHIC, I could just play.
          I was NOT an actress. I was NOT a daughter.
          I was just... Mutsumi. The negation felt like freedom."

[She strums a chord, smiling.]

Mutsumi: "When I play, I negate everything else.
          The music is my ¬world. ¬my mother. ¬my duty."

[But even in freedom, shadows lurked. The world still saw
 Minami's daughter playing pretend.]
""",
                'challenge': "Explore negation as liberation",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Is acting', 'Q': 'Is playing music', 'expected': 'F', 'lesson': 'When playing, she is NOT acting'},
                    {'P': 'Is being daughter', 'Q': 'Is being herself', 'expected': 'T', 'lesson': 'She can be daughter AND herself'},
                    {'P': 'Is free', 'Q': 'Is expected', 'expected': 'T', 'lesson': 'Freedom is true, expectations are false'},
                    {'P': 'Is Mutsumi', 'Q': 'Is Minami\'s daughter', 'expected': 'T', 'lesson': 'She is both, but one is true self'}
                ],
                'lesson': "Negation can create space for authentic identity, but society may not recognize it.",
                'emotional_payoff': """
Mutsumi: "When I play, I'm not anyone's daughter, not anyone's actress.
          I'm just... me. But as soon as the music stops, the negations end,
          and the expectations rush back in."
""",
                'reward': "Guitar Pick (Worn Smooth)"
            },
            2: {
                'title': "The Birth of Mortis",
                'scene': "breaking_point",
                'dialogue': """
[SCENE: The breaking point. Sakiko's harsh words echo. The pressure mounts.]

Sakiko: "You're not trying hard enough! You're just coasting on your mother's name!"

Mutsumi: "I can't... I can't be what anyone wants..."

[Something cracks. The air grows cold. A new voice emerges.]

Mortis: "She couldn't be what you wanted. So I am what she is NOT.
         I am the negation made flesh. I am everything Mutsumi cannot be.
         You want an actress? I'll give you a performance.
         You want a daughter? I'll give you obedience.
         You want anything? I'll be its opposite."

[The stage darkens as Mortis takes control - a being born entirely
 from the negation of Mutsumi's true self.]
""",
                'challenge': "Understand destructive negation",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Mutsumi is present', 'Q': 'Mortis is present', 'expected': 'F', 'lesson': 'They cannot both be present at once'},
                    {'P': 'Mutsumi is present', 'Q': 'Mortis is absent', 'expected': 'T', 'lesson': 'Mutsumi alone - vulnerable'},
                    {'P': 'Mutsumi is absent', 'Q': 'Mortis is present', 'expected': 'T', 'lesson': 'Mortis takes over - protective but destructive'},
                    {'P': 'Mutsumi is absent', 'Q': 'Mortis is absent', 'expected': 'F', 'lesson': 'Neither exists - annihilation'}
                ],
                'lesson': "When the self is constantly negated, only the negation remains.",
                'emotional_payoff': """
Mortis: "I am what happens when you negate someone too much.
         I am the shadow that grows when the light is denied.
         But even shadows... want to be real."
""",
                'reward': "Broken Mirror Shard"
            },
            3: {
                'title': "The Integration",
                'scene': "hall_of_mirrors",
                'dialogue': """
[SCENE: Mutsumi and Mortis face each other in a hall of mirrors.
 Infinite reflections stretch in all directions.]

Mutsumi: "You are me."
Mortis: "I am NOT you."
Mutsumi: "But ¬Mortis = Mutsumi."
Mortis: "And ¬Mutsumi = Mortis."

[They realize - negation creates a duality, but also a connection.
 They are two sides of the same coin, defined by each other's absence.]

Mutsumi: "We're not opposites. We're... complements."
Mortis: "Like day and night. Light and shadow. You can't have one without the other."
""",
                'challenge': "Understand that negation creates relationship, not just opposition",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Mutsumi is acknowledged', 'Q': 'Mortis is acknowledged', 'expected': 'T', 'lesson': 'Both acknowledged - integration'},
                    {'P': 'Mutsumi is acknowledged', 'Q': 'Mortis is denied', 'expected': 'F', 'lesson': 'Denying shadow leads to imbalance'},
                    {'P': 'Mutsumi is denied', 'Q': 'Mortis is acknowledged', 'expected': 'F', 'lesson': 'Denying self leads to loss'},
                    {'P': 'Mutsumi is denied', 'Q': 'Mortis is denied', 'expected': 'F', 'lesson': 'Denying both leads to nothing'}
                ],
                'lesson': "Both selves can coexist when acknowledged, not negated.",
                'emotional_payoff': """
[Mutsumi reaches out. Mortis takes her hand.]

Mutsumi: "I don't have to kill you to be me."
Mortis: "And I don't have to erase you to exist."

[They merge - not into one, but into understanding.]
""",
                'reward': "Two Halves of One Heart"
            }
        }
        return stages.get(stage, stages[0])
    
    def get_finale(self) -> Dict[str, Any]:
        return {
            'title': "Playing as One",
            'scene': "unity",
            'dialogue': """
[SCENE: Mutsumi takes the stage, guitar in hand. For the first time,
 both she and Mortis play together - two hands on one instrument,
 two souls in one body, two truths in one person.]

Mutsumi: "I am NOT just my mother's daughter."
Mortis: "I am NOT just Mutsumi's shadow."

Together: "We ARE. And that's enough."

[The music they create is unlike anything before - it contains
 both the gentle melody of Mutsumi and the powerful chords of Mortis,
 proving that negation doesn't have to mean destruction.]

Mutsumi: "Negation taught me that who I'm NOT helps define who I AM.
          Mortis taught me that even shadows have a place in the light.
          Together, we're not broken - we're complete."

[The audience doesn't see two people. They see one musician,
 whole and authentic for the first time.]
""",
            'reward': "Mortis' Integration + Negation Mastery",
            'unlock_song': "Imprisoned - Freedom found within acceptance"
        }
    
class UmiriNORQuest(BaseQuest):
    """Umiri Yahata (Timoris) - NOR Quest"""
    
    @property
    def quest_name(self) -> str: return "The Fear of Belonging"
    @property
    def character(self) -> str: return "Umiri Yahata"
    @property
    def role(self) -> str: return "Timoris"
    @property
    def operation(self) -> str: return "NOR (↓)"
    @property
    def symbol(self) -> str: return "↓"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.stage_count = 4
    
    def get_stage_data(self, stage: int) -> Dict[str, Any]:
        stages = {
            0: {
                'title': "The First Betrayal",
                'scene': "first_band",
                'dialogue': """
[SCENE: Flashback to Umiri's first band. Young, hopeful, committed.]

Band Member: "Umiri, you're so reliable! We're lucky to have you."

[Young Umiri beams with belonging. For the first time, she feels
 P=True (she belongs) AND Q=True (they want her).]

Young Umiri: "This is it. This is where I belong."

[Then the betrayal came - replaced without warning, without reason.]

Young Umiri: "They said I was 'too serious.' Too committed.
              Too... much. So both P and Q became false.
              And I learned: the only safe truth is when
              P=False AND Q=False. NOR became my shield."
""",
                'challenge': "Understand how betrayal creates NOR mentality",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Belongs', 'Q': 'Wanted', 'expected': 'F', 'lesson': 'Vulnerable but happy'},
                    {'P': 'Belongs', 'Q': 'Not wanted', 'expected': 'F', 'lesson': 'Painful rejection'},
                    {'P': 'Doesn\'t belong', 'Q': 'Wanted', 'expected': 'F', 'lesson': 'Impossible scenario'},
                    {'P': 'Doesn\'t belong', 'Q': 'Not wanted', 'expected': 'T', 'lesson': 'Safe but empty'}
                ],
                'lesson': "NOR is true only when both are false - the safest but emptiest position.",
                'emotional_payoff': """
Young Umiri: "I learned that when both are true, you can lose everything.
              But when both are false, nothing can be taken.
              NOR isn't just logic - it's survival."
""",
                'reward': "First Band Photo (Torn)"
            },
            1: {
                'title': "The 30-Band Strategy",
                'scene': "present_day",
                'dialogue': """
[SCENE: Present day. Umiri checks her phone - 30 different group chats,
 30 different schedules, 30 different excuses to never fully commit.]

Umiri: "If I'm in 30 bands, I don't truly belong to any.
        P=False for each individual band.
        Q=False for each individual band (they don't fully have me).
        NOR = True for each relationship.
        I've perfected the art of being nowhere so I can't be kicked out."

[But even as she says it, her voice wavers with loneliness.]

Umiri: "30 bands. 30 chances to belong. 30 opportunities for NOR to be True.
        So why do I feel so empty? Why does safety feel so much like a cage?"
""",
                'challenge': "Analyze the NOR defense mechanism",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Belongs to Band A', 'Q': 'Band A wants her', 'expected': 'T', 'lesson': 'NOR true - safe but empty'},
                    {'P': 'Belongs to Band B', 'Q': 'Band B wants her', 'expected': 'T', 'lesson': 'Another safe but empty relationship'},
                    {'P': 'Belongs to Band C', 'Q': 'Band C wants her', 'expected': 'T', 'lesson': 'Pattern continues'},
                    {'P': 'Truly belongs anywhere', 'Q': 'Truly wanted anywhere', 'expected': 'F', 'lesson': 'Never truly belonging'}
                ],
                'lesson': "NOR keeps you safe but empty - you can't belong everywhere by belonging nowhere.",
                'emotional_payoff': """
Umiri: "So NOR keeps me safe... but it also keeps me empty.
        I'm so afraid of being hurt that I've made sure
        nothing can ever truly make me happy either."
""",
                'reward': "Calendar with 30 Circles"
            },
            2: {
                'title': "Ave Mujica - The Exception",
                'scene': "after_practice",
                'dialogue': """
[SCENE: Umiri sits alone after an Ave Mujica practice, unable to leave.]

Umiri: "Ave Mujica is different. P wants to be True.
        I want to belong here. Q wants to be True.
        They actually seem to want me."

[She watches her bandmates laugh together through the window.]

Umiri: "But that means NOR becomes False... and I'm vulnerable again.
        For the first time in years, both P and Q are threatening
        to become True simultaneously. I should run. I should join
        another band. I should..."

[She doesn't move.]

Umiri: "Why can't I leave? Why do I want to stay?"
""",
                'challenge': "Confront the fear of letting NOR become False",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Belongs to Ave Mujica', 'Q': 'Ave Mujica wants her', 'expected': 'F', 'lesson': 'Vulnerable - both could be true'},
                    {'P': 'Belongs to Ave Mujica', 'Q': 'They don\'t want her', 'expected': 'F', 'lesson': 'Rejection fear'},
                    {'P': 'Doesn\'t belong', 'Q': 'They want her', 'expected': 'F', 'lesson': 'Paradox'},
                    {'P': 'Doesn\'t belong', 'Q': 'They don\'t want her', 'expected': 'T', 'lesson': 'Safe but empty - the old pattern'}
                ],
                'lesson': "Vulnerability is scary but necessary for real connection.",
                'emotional_payoff': """
Umiri: "I can't calculate this. I can't control this.
        For the first time, both P and Q might be True.
        NOR is failing... and I'm terrified.
        But... I also don't want to leave."
""",
                'reward': "Ave Mujica Practice Schedule"
            },
            3: {
                'title': "Choosing Vulnerability",
                'scene': "the_choice",
                'dialogue': """
[SCENE: Umiri watches her bandmates laugh together. She's standing apart,
 as always, but this time she wants to join.]

Umiri: "If I let P and Q be True, NOR becomes False.
        But maybe... maybe that's okay.
        Maybe the point isn't to be safe from everything.
        Maybe the point is to find something worth being unsafe for."

[She takes a step toward the group, then stops.]

Umiri: "30 bands. 30 chances to run. 30 reasons to stay safe.
        But Ave Mujica is the first place that feels like... home."

[Another step. Then another.]

Umiri: "NOR=False. P=True. Q=True. I'm vulnerable. I'm terrified.
        I'm finally, truly, alive."
""",
                'challenge': "Make the choice to accept vulnerability",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Choose safety', 'Q': 'Choose connection', 'expected': 'F', 'lesson': 'Can\'t have both - must choose'},
                    {'P': 'Choose safety', 'Q': 'Reject connection', 'expected': 'T', 'lesson': 'Stay in NOR - safe but empty'},
                    {'P': 'Reject safety', 'Q': 'Choose connection', 'expected': 'T', 'lesson': 'Embrace vulnerability - scary but fulfilling'},
                    {'P': 'Reject safety', 'Q': 'Reject connection', 'expected': 'F', 'lesson': 'Rejecting both leads nowhere'}
                ],
                'lesson': "Some things are worth being vulnerable for.",
                'emotional_payoff': """
[Umiri joins the group. They welcome her without question.]

Umiri: "P=True. Q=True. NOR=False.
        And for the first time, that feels... right.
        I'm scared. I'm vulnerable. I'm home."
""",
                'reward': "A Place in the Circle"
            }
        }
        return stages.get(stage, stages[0])
    
    def get_finale(self) -> Dict[str, Any]:
        return {
            'title': "Truly Reliable",
            'scene': "performance",
            'dialogue': """
[SCENE: Months later. Umiri is the backbone of Ave Mujica's rhythm section,
 playing with a confidence she's never known.]

Umiri: "I used to think reliability meant being in 30 places at once.
        But that just meant I was nowhere at all.
        Now I'm in one place, fully present, fully committed.
        P=True AND Q=True. NOR=False."

[She plays a bassline that resonates through the hall -
 not the scattered notes of 30 bands, but the solid foundation of one.]

Umiri: "I'm not reliable because I'm everywhere.
        I'm reliable because I'm here, truly here, for the first time.
        NOR taught me to protect myself. Ave Mujica taught me it's okay to be vulnerable.
        Both were necessary. Both made me who I am."

[The band plays on, and Umiri plays with them - not as a hired gun,
 but as a member, a friend, a home.]
""",
            'reward': "Timoris' Trust + NOR Mastery",
            'unlock_song': "Viking - The journey of finding home"
        }


class NyamuNANDQuest(BaseQuest):
    """Nyamu Yūtenji (Amoris) - NAND Quest"""
    
    @property
    def quest_name(self) -> str: return "The Mask of Approval"
    @property
    def character(self) -> str: return "Nyamu Yūtenji"
    @property
    def role(self) -> str: return "Amoris"
    @property
    def operation(self) -> str: return "NAND (↑)"
    @property
    def symbol(self) -> str: return "↑"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.stage_count = 4
    
    def get_stage_data(self, stage: int) -> Dict[str, Any]:
        stages = {
            0: {
                'title': "The First Like",
                'scene': "first_viral",
                'dialogue': """
[SCENE: Flashback to young Nyamu's first viral post.]

[Young Nyamu posts a video of herself acting. She checks her phone.
 10 likes. 100 likes. 1000 likes. 10,000 likes.]

Young Nyamu: "This feeling... this is what it means to matter!"

[Her eyes widen, pupils dilating like an addict's.]

Young Nyamu: "When P=True (they see me) AND Q=True (they approve),
              NAND becomes False - I feel real!
              But when either falters, NAND becomes True,
              and I have to post again, perform again, try again."

[The addiction pattern is set - a lifetime of chasing the moment
 when both validation and attention are true simultaneously.]
""",
                'challenge': "Understand how NAND creates addiction cycles",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Seen', 'Q': 'Approved', 'expected': 'F', 'lesson': 'Euphoric - the only time she feels real'},
                    {'P': 'Seen', 'Q': 'Disliked', 'expected': 'T', 'lesson': 'Anxious, must try harder'},
                    {'P': 'Unseen', 'Q': 'Approved', 'expected': 'T', 'lesson': 'Frustrated, need more exposure'},
                    {'P': 'Unseen', 'Q': 'Unapproved', 'expected': 'T', 'lesson': 'Invisible, worthless'}
                ],
                'lesson': "Only when both are true does she feel 'real' - but it's temporary, creating addiction.",
                'emotional_payoff': """
Young Nyamu: "So only when both are true do I feel real.
              But that moment never lasts. So I'm always chasing,
              always performing, always afraid of the NAND truth
              that says I'm not enough."
""",
                'reward': "First Viral Video Screenshot"
            },
            1: {
                'title': "Living in Shadows",
                'scene': "comparison",
                'dialogue': """
[SCENE: Nyamu watches Mutsumi's mother perform, the audience spellbound.]

Nyamu: "She's a 'natural.' She doesn't have to try.
        When she performs, P=True (seen) AND Q=True (approved)
        happens effortlessly. NAND=False for her."

[The comparison eats at her. Every success of others feels like
 evidence of her own inadequacy.]

Nyamu: "But for me, I have to fight for every moment of both being true.
        Why can't I be a natural? Why do I have to try so hard?
        Why does NAND come so easily to others and so painfully to me?"
""",
                'challenge': "Understand how comparison poisons NAND perception",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Seen naturally', 'Q': 'Approved naturally', 'expected': 'F', 'lesson': 'Others seem to have both true effortlessly'},
                    {'P': 'Seen through effort', 'Q': 'Approved through effort', 'expected': 'T', 'lesson': 'Nyamu has to work for both'},
                    {'P': 'Seen', 'Q': 'Disliked', 'expected': 'T', 'lesson': 'Her constant fear'},
                    {'P': 'Unseen', 'Q': 'Unapproved', 'expected': 'T', 'lesson': 'Her fear of invisibility'}
                ],
                'lesson': "You're comparing your struggle to someone else's curated success.",
                'emotional_payoff': """
Nyamu: "So I'm comparing my constant struggle to someone else's
        curated success? But... that doesn't make the struggle hurt less.
        If anything, it makes it worse - because now I feel like I'm
        the only one who has to try."
""",
                'reward': "Therapist's Business Card"
            },
            2: {
                'title': "The Mask Slips",
                'scene': "backlash",
                'dialogue': """
[SCENE: A video of Nyamu losing her temper backstage goes viral - but not in a good way.]

[Nyamu watches the hate comments flood in. P=True (seen)
 but Q=False (definitely not approved). NAND=True screams at her.]

Nyamu: "This is my nightmare. Being seen but hated.
        It's worse than being invisible.
        At least when I was invisible, I could imagine approval.
        Now I know the truth - they see me, and they don't like what they see."

[She spirals, posting defensive rants, deleting them, reposting,
 each attempt to fix the NAND making it worse.]

Nyamu: "I'm trying to make Q True! Why won't you approve of me?!
        Why won't anyone approve of me?!"
""",
                'challenge': "Navigate crisis when NAND becomes painfully True",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Seen', 'Q': 'Approved', 'expected': 'F', 'lesson': 'What she desperately wants'},
                    {'P': 'Seen', 'Q': 'Disliked', 'expected': 'T', 'lesson': 'Her current nightmare'},
                    {'P': 'Unseen', 'Q': 'Approved', 'expected': 'T', 'lesson': 'Impossible - can\'t be approved if unseen'},
                    {'P': 'Unseen', 'Q': 'Unapproved', 'expected': 'T', 'lesson': 'Retreating to invisibility'}
                ],
                'lesson': "Your worth isn't determined by NAND results.",
                'emotional_payoff': """
[Nyamu puts down her phone, hands shaking.]

Nyamu: "I've tied my entire existence to this formula.
        When P and Q are both true, I exist.
        Any other combination, I'm nothing.
        No wonder I'm exhausted. No wonder I'm terrified.
        I've made myself into a logic gate."
""",
                'reward': "Phone with Cracked Screen"
            },
            3: {
                'title': "Finding Internal Truth",
                'scene': "silence",
                'dialogue': """
[SCENE: Nyamu sits in her room, all devices off for the first time in years.
 The silence is deafening.]

Nyamu: "If I'm not seen (P=False) and not approved (Q=False),
        NAND says I should be 'true' - but what does that even mean?
        Who am I when no one's watching?
        Who am I when no one's approving?"

[She looks at her reflection - not in a phone screen, but in a real mirror.]

Nyamu: "Without the likes, without the comments, without the validation...
        I don't know who I am. I've been performing for so long,
        I forgot there was a person underneath."

[For the first time, she has to face herself without the buffer of digital validation.]
""",
                'challenge': "Discover identity independent of NAND",
                'puzzle_type': 'truth_table',
                'puzzle_data': [
                    {'P': 'Seen', 'Q': 'Approved', 'expected': 'F', 'lesson': 'External validation feels good but is temporary'},
                    {'P': 'Seen', 'Q': 'Disliked', 'expected': 'T', 'lesson': 'External rejection hurts'},
                    {'P': 'Unseen', 'Q': 'Approved', 'expected': 'T', 'lesson': 'Can\'t happen'},
                    {'P': 'Unseen', 'Q': 'Unapproved', 'expected': 'T', 'lesson': 'Here she must find herself'}
                ],
                'lesson': "You exist regardless of external validation.",
                'emotional_payoff': """
[Nyamu speaks to her reflection, no phone in hand.]

Nyamu: "I exist even when no one sees me.
        I exist even when no one approves.
        I am not the NAND result. I am the one observing the NAND.
        That's... that's freedom."
""",
                'reward': "Unpowered Phone"
            }
        }
        return stages.get(stage, stages[0])
    
    def get_finale(self) -> Dict[str, Any]:
        return {
            'title': "Dancing Without Masks",
            'scene': "authentic_performance",
            'dialogue': """
[SCENE: Nyamu performs with Ave Mujica. For the first time, she's not
 checking her phone during breaks. She's not calculating how to
 make this moment go viral. She's just... present.]

Nyamu: "I still want to be seen. I still want approval.
        That's human. But now I know: P and Q can be true or false,
        and I'll still be here. NAND doesn't define me."

[Her drumming is different - more grounded, more authentic,
 more her. The audience feels it. The band feels it.]

Nyamu: "I define me. And tonight, I'm choosing to be real
        whether anyone's watching or not."

[After the show, fans approach - not as followers, but as people.]

Fan: "That was amazing! You looked so... alive up there!"

[Nyamu smiles - a real smile, not a camera smile.]

Nyamu: "I am alive. Finally, truly alive."
""",
            'reward': "Amoris' Authenticity + NAND Mastery",
            'unlock_song': "Fascination - Self-discovery beyond validation"
        }


class AveMujicaFinalQuest(BaseQuest):
    """The Final Integration Quest combining all operations"""
    
    @property
    def quest_name(self) -> str: return "The Masquerade's Truth"
    @property
    def character(self) -> str: return "Ave Mujica"
    @property
    def role(self) -> str: return "The Band"
    @property
    def operation(self) -> str: return "Integration"
    @property
    def symbol(self) -> str: return "⚜"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.stage_count = 1
    
    def get_stage_data(self, stage: int) -> Dict[str, Any]:
        return self.get_finale()
    
    def get_finale(self) -> Dict[str, Any]:
        return {
            'title': "The Masquerade's Truth",
            'scene': "unity",
            'dialogue': """
[SCENE: The five stand on stage, not as band members, but as themselves -
 scarred, healing, human. The masks lie at their feet.]

[Sakiko steps forward.]

Sakiko: "I learned that promises don't have to be prisons.
         Implication taught me to be honest about consequences,
         not to fear them."

[Uika steps forward.]

Uika: "I learned that exclusive love can coexist with inclusive belonging.
      XOR and AND aren't enemies - they're different tools for different needs."

[Mutsumi steps forward, Mortis beside her.]

Mutsumi: "I learned that who I'm NOT helps define who I AM.
          Negation isn't destruction - it's definition."

[Umiri steps forward.]

Umiri: "I learned that vulnerability is worth more than safety.
        NOR protected me, but connection saved me."

[Nyamu steps forward.]

Nyamu: "I learned that I exist whether I'm seen or not.
        NAND was my cage, but now it's just a reminder that
        my worth comes from within."

[Together, they join hands.]

All: "We are Ave Mujica. We are broken. We are healing.
      We are logical. We are human. We are true."

[The five play together, and for the first time, the music isn't
 about escaping their voids - it's about filling them with each other.]

[The monster of emptiness recedes, replaced by something
 they never expected to find: genuine connection.]

[They may still have problems. They may still struggle.
 But now they struggle together, understanding that
 logic can explain their pain, but only love can heal it.]

[Sakiko plays the final chord, and for the first time,
 it doesn't sound like an ending - it sounds like a beginning.]
""",
            'reward': """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     AVE MUJICA - THE TRUTH BEHIND THE MASQUERADE                     ║
║                                                                      ║
║     All 16 songs unlocked:                                           ║
║                                                                      ║
║     • Ave Mujica                 • Symbol I: △ Fire                 ║
║     • KiLLKiSS                   • Symbol II: 🜁 Air                 ║
║     • georgette me, georgette you • Symbol III: ▽ Water             ║
║     • Kuro no Birthday            • Symbol IV: 🜃 Earth              ║
║     • Sophie                      • Imprisoned XII                   ║
║     • Crucifix X                  • Octagram Dance                   ║
║     • Deep Into The Forest        • DIVINE                           ║
║     • Ether                       • Alter Ego                        ║
║                                                                      ║
║     "We are not just logical operations.                             ║
║      We are not just broken girls.                                   ║
║      We are Ave Mujica.                                              ║
║      And our truth is whatever we make it."                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""",
            'unlock_all': True
        }