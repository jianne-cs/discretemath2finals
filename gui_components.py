# gui_components.py
# Main GUI application class with improved structure
# At the top of gui_components.py, update the import to:
from quest_system import CharacterQuestSystem, WindowManager, UIBuilder, PuzzleManager, QuestStatus, QuestStatusInfo
import tkinter as tk
from tkinter import ttk, font
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

from config import COLORS
from tutorial import LogicTutorial
from character_quests import (
    SakikoImplicationQuest, UikaXORQuest, MutsumiNegationQuest,
    UmiriNORQuest, NyamuNANDQuest, AveMujicaFinalQuest
)
from quest_system import CharacterQuestSystem, WindowManager, UIBuilder, PuzzleManager, QuestStatus, QuestStatusInfo


class SectionManager:
    """Manages scrolling to different sections"""
    
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.section_positions = {
            0: 0.0,    # Intro
            1: 0.2,    # Truth Cathedral
            2: 0.45,   # Character Encounters
            3: 0.7     # 16 Gates
        }
    
    def scroll_to(self, section_id: int) -> None:
        """Scroll to a specific section"""
        if section_id in self.section_positions:
            self.canvas.yview_moveto(self.section_positions[section_id])


class CharacterData:
    """Manages character data"""
    
    def __init__(self):
        self.data = {
            'Sakiko Togawa': {
                'role': 'Oblivionis',
                'instrument': 'Keyboards',
                'color': '#8A6E8E',
                'preposition': 'Implication (→)',
                'symbol': '→',
                'description': 'Implication is false ONLY when the first is true and second is false.',
                'quote': "IF a promise is made, THEN it must be kept... but at what cost?",
                'situation': "Oblivionis sits at her keyboard, torn between duty and desire...",
                'image': '🎹'
            },
            'Uika Misumi': {
                'role': 'Doloris',
                'instrument': 'Lead Guitar & Vocals',
                'color': '#9E7B9B',
                'preposition': 'XOR (⊕)',
                'symbol': '⊕',
                'description': 'XOR is true when exactly one statement is true.',
                'quote': "Love must be exclusive... or so I thought.",
                'situation': "Doloris's voice echoes with the pain of isolation...",
                'image': '🎸'
            },
            'Mutsumi Wakaba': {
                'role': 'Mortis',
                'instrument': 'Rhythm Guitar',
                'color': '#7D5D7A',
                'preposition': 'Negation (¬)',
                'symbol': '¬',
                'description': 'Negation reverses the truth value of a statement.',
                'quote': "I am NOT who they want me to be... but who am I?",
                'situation': "Mortis's shadow moves independently of her body...",
                'image': '🎸'
            },
            'Umiri Yahata': {
                'role': 'Timoris',
                'instrument': 'Bass',
                'color': '#6B4F68',
                'preposition': 'NOR (↓)',
                'symbol': '↓',
                'description': 'NOR is true only when both statements are false.',
                'quote': "If I belong to nothing, nothing can reject me...",
                'situation': "Timoris's bass resonates with the fear of commitment...",
                'image': '🎸'
            },
            'Nyamu Yūtenji': {
                'role': 'Amoris',
                'instrument': 'Drums',
                'color': '#A4839F',
                'preposition': 'NAND (↑)',
                'symbol': '↑',
                'description': 'NAND is false only when both statements are true.',
                'quote': "I only feel real when I'm seen AND approved...",
                'situation': "Amoris's drumming seeks validation from empty screens...",
                'image': '🥁'
            }
        }
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __iter__(self):
        return iter(self.data.items())
    
    def keys(self):
        return self.data.keys()
    
    def values(self):
        return self.data.values()
    
    def items(self):
        return self.data.items()
    
    def __len__(self):
        """Return the number of characters"""
        return len(self.data)


class LogicalOperationsData:
    """Manages logical operations data"""
    
    def __init__(self):
        self.operations = [
            {
                'name': 'Contradiction',
                'symbol': '⊥',
                'truth_table': [False, False, False, False],
                'description': 'Always false, regardless of input',
                'type': 'Nullary'
            },
            {
                'name': 'NOR',
                'symbol': '↓',
                'truth_table': [True, False, False, False],
                'description': 'True only when both are false',
                'type': 'Joint denial'
            },
            {
                'name': 'Converse Nonimplication',
                'symbol': '↚',
                'truth_table': [False, True, False, False],
                'description': 'True only when Q is true and P is false',
                'type': 'Conditional'
            },
            {
                'name': 'Negation of P',
                'symbol': '¬P',
                'truth_table': [True, True, False, False],
                'description': 'True when P is false',
                'type': 'Unary'
            },
            {
                'name': 'Material Nonimplication',
                'symbol': '↛',
                'truth_table': [False, False, True, False],
                'description': 'True only when P is true and Q is false',
                'type': 'Conditional'
            },
            {
                'name': 'Negation of Q',
                'symbol': '¬Q',
                'truth_table': [True, False, True, False],
                'description': 'True when Q is false',
                'type': 'Unary'
            },
            {
                'name': 'XOR',
                'symbol': '⊕',
                'truth_table': [False, True, True, False],
                'description': 'True when exactly one is true',
                'type': 'Exclusive'
            },
            {
                'name': 'NAND',
                'symbol': '↑',
                'truth_table': [True, True, True, False],
                'description': 'False only when both are true',
                'type': 'Alternative denial'
            },
            {
                'name': 'AND',
                'symbol': '∧',
                'truth_table': [False, False, False, True],
                'description': 'True only when both are true',
                'type': 'Conjunction'
            },
            {
                'name': 'XNOR',
                'symbol': '↔',
                'truth_table': [True, False, False, True],
                'description': 'True when both are the same',
                'type': 'Biconditional'
            },
            {
                'name': 'Projection Q',
                'symbol': 'Q',
                'truth_table': [False, True, False, True],
                'description': 'Simply Q, ignores P',
                'type': 'Projection'
            },
            {
                'name': 'Implication',
                'symbol': '→',
                'truth_table': [True, True, False, True],
                'description': 'False only when P is true and Q is false',
                'type': 'Conditional'
            },
            {
                'name': 'Projection P',
                'symbol': 'P',
                'truth_table': [False, False, True, True],
                'description': 'Simply P, ignores Q',
                'type': 'Projection'
            },
            {
                'name': 'Converse Implication',
                'symbol': '←',
                'truth_table': [True, False, True, True],
                'description': 'False only when Q is true and P is false',
                'type': 'Conditional'
            },
            {
                'name': 'OR',
                'symbol': '∨',
                'truth_table': [False, True, True, True],
                'description': 'False only when both are false',
                'type': 'Disjunction'
            },
            {
                'name': 'Tautology',
                'symbol': '⊤',
                'truth_table': [True, True, True, True],
                'description': 'Always true, regardless of input',
                'type': 'Nullary'
            }
        ]
    
    def __getitem__(self, index):
        return self.operations[index]
    
    def __len__(self):
        return len(self.operations)
    
    def __iter__(self):
        return iter(self.operations)
    
    def index(self, item):
        """Return the index of an item in the operations list"""
        return self.operations.index(item)


class SongsData:
    """Manages Ave Mujica songs data"""
    
    def __init__(self):
        self.songs = [
            {
                'title': 'Gehaburn',
                'operation': 'Implication',
                'meaning': 'If you burn, then you must feel the pain',
                'color': '#8B0000',
                'lyric': "If the flame consumes, then despair follows..."
            },
            {
                'title': 'Angles',
                'operation': 'XOR',
                'meaning': 'Angels exist if and only if we believe',
                'color': '#4A2C2C',
                'lyric': "Heaven and earth are one and the same..."
            },
            {
                'title': 'Imprisoned',
                'operation': 'Negation',
                'meaning': 'Freedom found within acceptance',
                'color': '#2D1B1B',
                'lyric': "I am not who they want me to be..."
            },
            {
                'title': 'Viking',
                'operation': 'NOR',
                'meaning': 'The journey of finding home',
                'color': '#5C3A3A',
                'lyric': "If I belong to nothing, nothing can reject me..."
            },
            {
                'title': 'Fascination',
                'operation': 'NAND',
                'meaning': 'Self-discovery beyond validation',
                'color': '#6B4C4C',
                'lyric': "I only feel real when I'm seen AND approved..."
            }
        ]
    
    def __getitem__(self, index):
        return self.songs[index]
    
    def __len__(self):
        return len(self.songs)
    
    def __iter__(self):
        return iter(self.songs)


class QuizManager:
    """Manages quiz state and logic"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_operation_index = 0
        self.score = 0
        self.questions_answered = 0
        self.total_questions = 16
        self.correct_streak = 0
        self.answer_submitted = False
        self.selected_answer = None
        self.selected_button = None
        
        self.score_display = None
        self.streak_display = None
        self.truth_display = None
        self.operation_label = None
        self.options_frame = None
    
    def new_quiz(self):
        """Start a new quiz round"""
        if self.questions_answered < self.total_questions:
            # Get unlocked operations based on completed quests
            unlocked_operations = []
            for character, completed in self.parent.quest_system.quest_completed.items():
                if completed:
                    quest = self.parent.quest_system.quests.get(character)
                    if quest:
                        unlocked_operations.append(quest.operation.split()[0])
            
            # Find available operations
            available_ops = [op for op in self.parent.logical_operations 
                            if op['name'] not in unlocked_operations]
            
            if available_ops:
                self.current_operation_index = random.randint(0, len(available_ops) - 1)
                current_op = available_ops[self.current_operation_index]
            else:
                self.current_operation_index = random.randint(
                    0, len(self.parent.logical_operations) - 1
                )
                current_op = self.parent.logical_operations[self.current_operation_index]
            
            self.display_current_truth_table(current_op)
    
    def display_current_truth_table(self, operation):
        """Display current truth table for quiz"""
        if not hasattr(self, 'truth_display') or not self.truth_display:
            return
        
        # Clear previous display
        for widget in self.truth_display.winfo_children():
            widget.destroy()
        
        # Operation name
        op_label = tk.Label(self.truth_display, text=f"Operation: {operation['name']} {operation['symbol']}",
                           font=('Georgia', 14, 'bold'), fg=COLORS['gold'], bg=COLORS['ebony'])
        op_label.pack(pady=10)
        
        # Description
        desc_label = tk.Label(self.truth_display, text=operation['description'],
                             font=('Georgia', 10), fg=COLORS['periwinkle'], bg=COLORS['ebony'],
                             wraplength=600)
        desc_label.pack(pady=5)
        
        # Create truth table
        table_frame = tk.Frame(self.truth_display, bg=COLORS['cream'])
        table_frame.pack(pady=10)
        
        # Headers
        headers = ['P', 'Q', 'Result']
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, font=('Georgia', 11, 'bold'),
                           bg=COLORS['periwinkle'], fg=COLORS['deep_red'],
                           relief='raised', borderwidth=2, width=10, height=2)
            label.grid(row=0, column=i, padx=1, pady=1)
        
        # Input values
        p_values = [False, False, True, True]
        q_values = [False, True, False, True]
        
        for row in range(4):
            # P
            tk.Label(table_frame, text='T' if p_values[row] else 'F',
                    font=('Courier', 11, 'bold'), bg=COLORS['cream'],
                    fg=COLORS['deep_red'], width=10, height=2,
                    relief='sunken').grid(row=row+1, column=0, padx=1, pady=1)
            
            # Q
            tk.Label(table_frame, text='T' if q_values[row] else 'F',
                    font=('Courier', 11, 'bold'), bg=COLORS['cream'],
                    fg=COLORS['deep_red'], width=10, height=2,
                    relief='sunken').grid(row=row+1, column=1, padx=1, pady=1)
            
            # Result
            result = '?' if not self.answer_submitted else ('T' if operation['truth_table'][row] else 'F')
            result_label = tk.Label(table_frame, text=result,
                                   font=('Courier', 11, 'bold'), bg=COLORS['cream'],
                                   fg=COLORS['wine'], width=10, height=2,
                                   relief='sunken')
            result_label.grid(row=row+1, column=2, padx=1, pady=1)
        
        # Answer options
        if not self.answer_submitted:
            self.options_frame = tk.Frame(self.truth_display, bg=COLORS['ebony'])
            self.options_frame.pack(pady=10)
            
            tk.Label(self.options_frame, text="Select the correct truth table pattern:",
                    font=('Georgia', 10), fg=COLORS['cream'], bg=COLORS['ebony']).pack()
            
            # Create option buttons
            options_frame = tk.Frame(self.options_frame, bg=COLORS['ebony'])
            options_frame.pack(pady=5)
            
            # Generate 4 possible truth table patterns (one correct, three random)
            correct_pattern = ''.join(['T' if x else 'F' for x in operation['truth_table']])
            options = [correct_pattern]
            
            # Add random wrong options
            while len(options) < 4:
                random_pattern = ''.join(random.choice(['T', 'F']) for _ in range(4))
                if random_pattern not in options:
                    options.append(random_pattern)
            
            random.shuffle(options)
            
            for i, option in enumerate(options):
                btn = tk.Button(options_frame, text=option,
                               command=lambda o=option: self.check_answer(o, correct_pattern),
                               bg=COLORS['deep_red'], fg=COLORS['gold'],
                               font=('Georgia', 10, 'bold'), width=10,
                               cursor='hand2')
                btn.grid(row=i//2, column=i%2, padx=5, pady=5)
        
        self.update_displays()
    
    def check_answer(self, selected, correct):
        """Check quiz answer"""
        if self.answer_submitted:
            return
        
        self.answer_submitted = True
        self.selected_answer = selected
        
        if selected == correct:
            self.score += 1
            self.correct_streak += 1
            result_text = "✓ CORRECT!"
            result_color = COLORS['success_green']
            
            # Unlock song if this was a new operation
            current_op = self.parent.logical_operations[self.current_operation_index]
            if current_op['name'] not in [s['operation'] for s in self.parent.unlocked_songs]:
                for song in self.parent.ave_mujica_songs:
                    if song['operation'] == current_op['name'] and song not in self.parent.unlocked_songs:
                        self.parent.unlocked_songs.append(song)
                        break
        else:
            self.correct_streak = 0
            result_text = f"✗ INCORRECT. The correct pattern was {correct}"
            result_color = COLORS['error_red']
        
        self.questions_answered += 1
        
        # Show result
        result_label = tk.Label(self.truth_display, text=result_text,
                               font=('Georgia', 12, 'bold'), fg=result_color,
                               bg=COLORS['ebony'])
        result_label.pack(pady=10)
        
        # Next button
        if self.questions_answered < self.total_questions:
            next_btn = tk.Button(self.truth_display, text="Next Gate →",
                                command=self.next_question,
                                bg=COLORS['gold'], fg=COLORS['ebony'],
                                font=('Georgia', 11, 'bold'), cursor='hand2')
            next_btn.pack(pady=5)
        else:
            # Show completion
            completion_frame = tk.Frame(self.truth_display, bg=COLORS['gold'], bd=2, relief='raised')
            completion_frame.pack(pady=20, padx=20, fill=tk.X)
            
            tk.Label(completion_frame, 
                    text="🎉 CONGRATULATIONS! 🎉",
                    font=('Georgia', 16, 'bold'),
                    fg=COLORS['deep_red'], bg=COLORS['gold']).pack(pady=10)
            
            tk.Label(completion_frame,
                    text=f"You've unlocked all {len(self.parent.unlocked_songs)} songs!",
                    font=('Georgia', 12),
                    fg=COLORS['ebony'], bg=COLORS['gold']).pack(pady=5)
            
            tk.Label(completion_frame,
                    text="The complete truth is now yours...",
                    font=('Georgia', 10, 'italic'),
                    fg=COLORS['deep_red'], bg=COLORS['gold']).pack(pady=5)
        
        self.update_displays()
    
    def next_question(self):
        """Move to next quiz question"""
        self.answer_submitted = False
        self.selected_answer = None
        self.new_quiz()
    
    def update_displays(self):
        """Update score and streak displays"""
        if self.score_display:
            self.score_display.config(
                text=f"⚜ Grimoire Progress: {self.questions_answered}/{self.total_questions} ⚜"
            )
        if self.streak_display:
            self.streak_display.config(text=f"🔥 Streak: {self.correct_streak}")


class AveMujicaLogicGrimoire:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Ave Mujica - The Complete Logic Grimoire")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS['shadow'])
        
        # Make window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Initialize managers
        self.window_manager = WindowManager()
        self.ui_builder = UIBuilder()
        self.characters = CharacterData()
        self.logical_operations = LogicalOperationsData()
        self.ave_mujica_songs = SongsData()
        self.quiz_manager = QuizManager(self)
        
        # Initialize font families
        self.available_fonts = list(font.families())
        
        # Map operations to songs
        self.song_by_operation = {}
        for song in self.ave_mujica_songs:
            if song['operation'] not in self.song_by_operation:
                self.song_by_operation[song['operation']] = song
        
        # Current quiz state
        self.unlocked_songs = []
        
        # Initialize quest system
        self.quest_system = CharacterQuestSystem(self)
        
        # Set up quests
        quests_dict = {
            'Sakiko Togawa': SakikoImplicationQuest(self),
            'Uika Misumi': UikaXORQuest(self),
            'Mutsumi Wakaba': MutsumiNegationQuest(self),
            'Umiri Yahata': UmiriNORQuest(self),
            'Nyamu Yūtenji': NyamuNANDQuest(self)
        }
        final_quest = AveMujicaFinalQuest(self)
        self.quest_system.set_quests(quests_dict, final_quest)
        
        # UI references
        self.cards_frame = None
        self.canvas = None
        self.scrollable_frame = None
        self.section_manager = None
        self.songs_frame = None
        
        self.setup_styles()
        self.create_main_website()
    
    def setup_styles(self):
        """Configure custom gothic Victorian styles"""
        style = ttk.Style()
        
        style.configure('Gothic.TLabel', 
                       background=COLORS['shadow'],
                       foreground=COLORS['cream'])
        
        style.configure('Gothic.TButton',
                       background=COLORS['deep_red'],
                       foreground=COLORS['gold'])
        
        style.configure('Gothic.TFrame',
                       background=COLORS['shadow'])
        
        style.configure('Gothic.TLabelframe',
                       background=COLORS['shadow'],
                       foreground=COLORS['gold'],
                       relief='ridge',
                       borderwidth=3)
        
        style.configure('Gothic.TLabelframe.Label',
                       background=COLORS['shadow'],
                       foreground=COLORS['gold'])
        
        style.configure("black.Horizontal.TProgressbar", 
                       background=COLORS['gold'],
                       troughcolor=COLORS['shadow'])
    
    def create_main_website(self):
        """Create the main website with all sections"""
        
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS['ebony'])
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Navigation bar
        self.create_navigation(main_container)
        
        # Main content area with scrollable canvas
        self.create_scrollable_content(main_container)
        
        # Victorian status bar
        self.create_victorian_status(main_container)
    
    def create_navigation(self, parent):
        """Create centered navigation bar"""
        nav_frame = tk.Frame(parent, bg=COLORS['deep_red'], height=70)
        nav_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        nav_frame.grid_propagate(False)
        
        # Center navigation buttons
        nav_center = tk.Frame(nav_frame, bg=COLORS['deep_red'])
        nav_center.place(relx=0.5, rely=0.5, anchor='center')
        
        # Navigation buttons
        sections = [
            ("🏰 Intro", 0),
            ("⛪ Truth Cathedral", 1),
            ("👥 Character Quests", 2),
            ("🔮 16 Gates", 3)
        ]
        
        for text, section_id in sections:
            btn = tk.Button(nav_center, text=text,
                command=lambda s=section_id: self.section_manager.scroll_to(s),
                bg=COLORS['wine'], fg=COLORS['gold'],
                font=('Georgia', 11, 'bold'), relief='raised',
                borderwidth=2, padx=20, pady=8, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=10)
        
        # Quest Hub button
        quest_btn = tk.Button(nav_center, text="🔮 Quest Hub",
            command=self.open_quest_hub,
            bg=COLORS['crimson'], fg=COLORS['gold'],
            font=('Georgia', 11, 'bold'), relief='raised',
            borderwidth=2, padx=20, pady=8, cursor='hand2')
        quest_btn.pack(side=tk.LEFT, padx=10)
    
    def open_quest_hub(self):
        """Open the quest selection hub"""
        quest_hub = tk.Toplevel(self.root)
        quest_hub.title("Ave Mujica - Character Quests")
        quest_hub.configure(bg=COLORS['ebony'])
        quest_hub.transient(self.root)
        quest_hub.grab_set()
        
        self.window_manager.center_window(quest_hub, 1000, 800)
        self.quest_system.create_quest_selector(quest_hub)
    
    def create_scrollable_content(self, parent):
        """Create scrollable content area"""
        
        # Create canvas and scrollbar
        canvas_frame = tk.Frame(parent, bg=COLORS['shadow'])
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(canvas_frame, bg=COLORS['shadow'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        # Create main frame for content
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS['shadow'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="n", 
            width=self.canvas.winfo_width()
        )
        
        def update_canvas_width(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        
        self.canvas.bind('<Configure>', update_canvas_width)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mousewheel for scrolling
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Grid layout
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Initialize section manager
        self.section_manager = SectionManager(self.canvas)
        
        # Create content container
        content_container = tk.Frame(self.scrollable_frame, bg=COLORS['shadow'])
        content_container.pack(expand=True, fill=tk.BOTH)
        
        # Create all sections
        self.create_intro_section(content_container)
        self.create_scroll_divider(content_container, "First Revelation")
        self.create_truth_cathedral_section(content_container)
        self.create_scroll_divider(content_container, "Second Revelation")
        self.create_character_encounters_section(content_container)
        self.create_scroll_divider(content_container, "Final Revelation")
        self.create_gates_of_truth_section(content_container)
    
    def create_intro_section(self, parent):
        """Create the intro section"""
        section = tk.Frame(parent, bg=COLORS['shadow'])
        section.pack(fill=tk.X, pady=30, padx=50)
        
        # Ornate border
        border_frame = tk.Frame(section, bg=COLORS['gold'], bd=3, relief='ridge')
        border_frame.pack(fill=tk.X, padx=50)
        
        content = tk.Frame(border_frame, bg=COLORS['ebony'], bd=2, relief='sunken')
        content.pack(fill=tk.X, expand=True, padx=3, pady=3)
        
        # Title
        title_font = ('Edwardian Script ITC', 48) if 'Edwardian Script ITC' in self.available_fonts else ('Georgia', 40, 'bold')
        
        tk.Label(content, text="AVE MUJICA",
                font=title_font, fg=COLORS['gold'], bg=COLORS['ebony']).pack(pady=30)
        
        tk.Label(content, text="〚 The Complete Logic Grimoire 〛",
                font=('Georgia', 16, 'italic'), fg=COLORS['periwinkle'], bg=COLORS['ebony']).pack()
        
        # Welcome message
        welcome_text = "Welcome to the Gothic Masquerade of Logic...\n\n" + \
                      "Within these hallowed halls, five masked musicians await,\n" + \
                      "each guarding a fundamental truth of propositional logic.\n\n" + \
                      "🌟 NEW: Character Quests Available! 🌟\n" + \
                      "Embark on personal journeys with each band member\n" + \
                      "to master logical operations through their deepest struggles.\n\n" + \
                      "Journey through the Truth Cathedral,\n" + \
                      "Encounter each band member and begin their quest,\n" + \
                      "And unlock the 16 Gates of Truth to reveal all their songs.\n\n" + \
                      "Use the navigation above to begin your descent..."
        
        tk.Label(content, text=welcome_text,
                font=('Georgia', 12), fg=COLORS['cream'], bg=COLORS['ebony'],
                justify=tk.CENTER).pack(pady=30, padx=50)
        
        # Decorative elements
        tk.Label(content, text="⚜️  🦇  🌹  🕯️  🗝️  ⚜️",
                font=('Georgia', 20), fg=COLORS['gold'], bg=COLORS['ebony']).pack(pady=20)
    
    def create_scroll_divider(self, parent, title):
        """Create a decorative scroll divider"""
        section = tk.Frame(parent, bg=COLORS['scroll_bg'])
        section.pack(fill=tk.X, pady=40, padx=50)
        
        # Scroll-like design
        scroll_top = tk.Frame(section, bg=COLORS['cream'], height=20)
        scroll_top.pack(fill=tk.X, padx=100)
        
        tk.Label(scroll_top, text="⚜ ⚜ ⚜", 
                fg=COLORS['deep_red'], bg=COLORS['cream'],
                font=('Georgia', 12)).pack()
        
        scroll_middle = tk.Frame(section, bg=COLORS['periwinkle'], height=80)
        scroll_middle.pack(fill=tk.X, padx=100)
        
        title_font = ('Edwardian Script ITC', 24) if 'Edwardian Script ITC' in self.available_fonts else ('Georgia', 20, 'bold')
        
        tk.Label(scroll_middle, text=title,
                font=title_font, fg=COLORS['deep_red'], 
                bg=COLORS['periwinkle']).pack(expand=True)
        
        scroll_bottom = tk.Frame(section, bg=COLORS['cream'], height=20)
        scroll_bottom.pack(fill=tk.X, padx=100)
        
        tk.Label(scroll_bottom, text="⚜ ⚜ ⚜", 
                fg=COLORS['deep_red'], bg=COLORS['cream'],
                font=('Georgia', 12)).pack()
    
    def create_truth_cathedral_section(self, parent):
        """Create the Truth Cathedral section"""
        section = tk.Frame(parent, bg=COLORS['shadow'])
        section.pack(fill=tk.X, pady=30, padx=50)
        
        # Cathedral frame
        cathedral_frame = tk.Frame(section, bg=COLORS['gold'], bd=5, relief='ridge')
        cathedral_frame.pack(fill=tk.X, padx=50)
        
        content = tk.Frame(cathedral_frame, bg=COLORS['ebony'], bd=3, relief='sunken')
        content.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Title
        title_frame = tk.Frame(content, bg=COLORS['ebony'])
        title_frame.pack(pady=20)
        
        tk.Label(title_frame, text="⛪ TRUTH CATHEDRAL ⛪",
                font=('Georgia', 28, 'bold'), fg=COLORS['gold'], bg=COLORS['ebony']).pack()
        
        tk.Label(title_frame, text="Where All Logical Truths Are Revealed",
                font=('Georgia', 14, 'italic'), fg=COLORS['periwinkle'], bg=COLORS['ebony']).pack()
        
        # Tutorial button
        tk.Button(content, text="📚 OPEN LOGIC GRIMOIRE TUTORIAL 📚",
                 command=self.open_logic_tutorial,
                 bg=COLORS['crimson'], fg=COLORS['gold'],
                 font=('Georgia', 12, 'bold'),
                 relief='raised', borderwidth=3,
                 padx=20, pady=10, cursor='hand2').pack(pady=10)
        
        # Quick reference
        self._create_quick_reference(content)
        
        # Truth table
        self._create_truth_table_display(content)
        
        # Explanation
        explanation = "The Truth Cathedral displays all 16 possible logical operations for two propositions.\n" + \
                     "Each column represents a different logical connective, showing how truth flows through the gates.\n" + \
                     "Click the tutorial button above for detailed explanations with character stories!"
        
        tk.Label(content, text=explanation,
                font=('Georgia', 11, 'italic'), fg=COLORS['cream'], bg=COLORS['ebony'],
                justify=tk.CENTER).pack(pady=20)
    
    def _create_quick_reference(self, parent):
        """Create quick reference guide"""
        quick_ref = tk.Frame(parent, bg=COLORS['shadow'], bd=2, relief='ridge')
        quick_ref.pack(fill=tk.X, pady=10, padx=30)
        
        tk.Label(quick_ref, text="⚡ QUICK REFERENCE GUIDE ⚡",
                font=('Georgia', 14, 'bold'),
                fg=COLORS['gold'], bg=COLORS['shadow']).pack(pady=5)
        
        ref_text = """
        • AND (∧) : True ONLY when both are True
        • OR (∨)  : True when at least one is True
        • IMPLICATION (→) : False ONLY when True → False
        • BICONDITIONAL (↔) : True when both are the same
        • NEGATION (¬) : Reverses the truth value
        • XOR (⊕) : True when exactly one is True
        • NAND (↑) : False only when both are True
        • NOR (↓) : True only when both are False
        """
        
        tk.Label(quick_ref, text=ref_text,
                font=('Courier', 10), fg=COLORS['cream'], bg=COLORS['shadow'],
                justify=tk.LEFT).pack(pady=5, padx=20)
    
    def _create_truth_table_display(self, parent):
        """Create truth table display"""
        table_frame = tk.Frame(parent, bg=COLORS['cream'], bd=3, relief='raised')
        table_frame.pack(pady=20, padx=30, fill=tk.X)
        
        table_center = tk.Frame(table_frame, bg=COLORS['cream'])
        table_center.pack()
        
        # Table headers
        headers = ['P', 'Q', 'AND\n∧', 'OR\n∨', 'NOT P\n¬P', 'NOT Q\n¬Q', 
                  'P→Q\n→', 'P↔Q\n↔', 'XOR\n⊕', 'NAND\n↑', 'NOR\n↓']
        
        for i, header in enumerate(headers):
            label = tk.Label(table_center, text=header,
                           font=('Georgia', 10, 'bold'),
                           bg=COLORS['periwinkle'],
                           fg=COLORS['deep_red'],
                           relief='raised', borderwidth=2,
                           width=8, pady=8)
            label.grid(row=0, column=i, padx=1, pady=1)
        
        # Fill truth table
        row = 1
        for p in [True, False]:
            for q in [True, False]:
                values = [
                    'T' if p else 'F',
                    'T' if q else 'F',
                    'T' if (p and q) else 'F',
                    'T' if (p or q) else 'F',
                    'T' if (not p) else 'F',
                    'T' if (not q) else 'F',
                    'T' if ((not p) or q) else 'F',
                    'T' if (p == q) else 'F',
                    'T' if (p != q) else 'F',
                    'T' if (not (p and q)) else 'F',
                    'T' if (not (p or q)) else 'F'
                ]
                for col, val in enumerate(values):
                    label = tk.Label(table_center, text=val,
                                   font=('Courier', 10, 'bold'),
                                   bg=COLORS['cream'],
                                   fg=COLORS['wine'],
                                   relief='sunken', borderwidth=1,
                                   width=8, pady=5)
                    label.grid(row=row, column=col, padx=1, pady=1)
                row += 1
    
    def open_logic_tutorial(self):
        """Open the comprehensive logic tutorial window"""
        tutorial = LogicTutorial.get_tutorial_content()
        
        tutorial_window = tk.Toplevel(self.root)
        tutorial_window.title("Logic Grimoire Tutorial")
        tutorial_window.configure(bg=COLORS['ebony'])
        tutorial_window.transient(self.root)
        tutorial_window.grab_set()
        
        self.window_manager.center_window(tutorial_window, 900, 800)
        
        # Main frame
        main_frame = tk.Frame(tutorial_window, bg=COLORS['ebony'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text=tutorial['title'],
                font=('Georgia', 18, 'bold'),
                fg=COLORS['gold'], bg=COLORS['ebony']).pack(pady=10)
        
        # Introduction
        intro_frame = tk.Frame(main_frame, bg=COLORS['shadow'], bd=2, relief='ridge')
        intro_frame.pack(fill=tk.X, pady=10)
        
        intro_text = tk.Text(intro_frame, height=6,
                            bg=COLORS['shadow'], fg=COLORS['periwinkle'],
                            font=('Georgia', 10), wrap=tk.WORD,
                            padx=15, pady=15)
        intro_text.pack(fill=tk.X)
        intro_text.insert(tk.END, tutorial['introduction'])
        intro_text.config(state=tk.DISABLED)
        
        # Create notebook for sections
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add each section as a tab
        for section in tutorial['sections']:
            self._create_tutorial_tab(notebook, section)
        
        # Tips section
        tips_frame = tk.Frame(main_frame, bg=COLORS['shadow'], bd=2, relief='ridge')
        tips_frame.pack(fill=tk.X, pady=10)
        
        tips_text = tk.Text(tips_frame, height=10,
                           bg=COLORS['shadow'], fg=COLORS['gold'],
                           font=('Georgia', 10), wrap=tk.WORD,
                           padx=15, pady=15)
        tips_text.pack(fill=tk.X)
        tips_text.insert(tk.END, tutorial['tips'])
        tips_text.config(state=tk.DISABLED)
        
        # Close button
        tk.Button(main_frame, text="Close Tutorial",
                 command=tutorial_window.destroy,
                 bg=COLORS['deep_red'], fg=COLORS['gold'],
                 font=('Georgia', 11, 'bold'),
                 padx=20, pady=5, cursor='hand2').pack(pady=10)
    
    def _create_tutorial_tab(self, notebook, section):
        """Create a tutorial tab"""
        tab = tk.Frame(notebook, bg=COLORS['ebony'])
        notebook.add(tab, text=section['title'][:15] + "...")
        
        # Section content
        content_frame = tk.Frame(tab, bg=COLORS['ebony'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        tk.Label(content_frame, text=section['title'],
                font=('Georgia', 14, 'bold'),
                fg=COLORS['gold'], bg=COLORS['ebony']).pack(pady=5)
        
        # Character and symbol
        char_frame = tk.Frame(content_frame, bg=COLORS['shadow'], bd=2, relief='ridge')
        char_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(char_frame, text=f"{section['character']}  |  Symbol: {section['symbol']}",
                font=('Georgia', 11, 'italic'),
                fg=COLORS['periwinkle'], bg=COLORS['shadow']).pack(pady=5)
        
        # Description
        desc_frame = tk.Frame(content_frame, bg=COLORS['cream'], bd=2, relief='raised')
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        desc_text = tk.Text(desc_frame, height=12,
                           bg=COLORS['cream'], fg=COLORS['deep_red'],
                           font=('Georgia', 10), wrap=tk.WORD,
                           padx=15, pady=15)
        desc_text.pack(fill=tk.BOTH, expand=True)
        desc_text.insert(tk.END, section['description'])
        desc_text.config(state=tk.DISABLED)
        
        # Example
        example_frame = tk.Frame(content_frame, bg=COLORS['shadow'], bd=2, relief='ridge')
        example_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(example_frame, text=section['example'],
                font=('Georgia', 9, 'italic'),
                fg=COLORS['cream'], bg=COLORS['shadow']).pack(pady=5)
    
    def create_character_encounters_section(self, parent):
        """Create the Character Encounters section"""
        section = tk.Frame(parent, bg=COLORS['shadow'])
        section.pack(fill=tk.X, pady=30, padx=50)
        
        # Main frame
        main_frame = tk.Frame(section, bg=COLORS['gold'], bd=5, relief='ridge')
        main_frame.pack(fill=tk.X, padx=50)
        
        content = tk.Frame(main_frame, bg=COLORS['ebony'], bd=3, relief='sunken')
        content.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Title
        title_frame = tk.Frame(content, bg=COLORS['ebony'])
        title_frame.pack(pady=20)
        
        tk.Label(title_frame, text="👥 CHARACTER QUESTS 👥",
                font=('Georgia', 26, 'bold'), fg=COLORS['gold'], bg=COLORS['ebony']).pack()
        
        tk.Label(title_frame, text="Embark on Personal Journeys with Each Band Member",
                font=('Georgia', 14, 'italic'), fg=COLORS['periwinkle'], bg=COLORS['ebony']).pack()
        
        # Quest progress summary
        self._create_quest_progress_summary(content)
        
        # Cards frame
        self.cards_frame = tk.Frame(content, bg=COLORS['ebony'])
        self.cards_frame.pack(pady=20)
        
        # Create character cards
        self.refresh_character_encounters()
        
        # Description
        description = "Each character guards a fundamental logical operation and has a personal quest.\n" + \
                     "Complete their quests to unlock deeper meanings of their songs and master the operations.\n" + \
                     "Click on any character card to begin their journey."
        
        tk.Label(content, text=description,
                font=('Georgia', 11, 'italic'), fg=COLORS['cream'], bg=COLORS['ebony'],
                justify=tk.CENTER).pack(pady=20)
    
    def _create_quest_progress_summary(self, parent):
        """Create quest progress summary"""
        completed = sum(1 for c in self.quest_system.quest_completed.values() if c)
        total = len(self.characters)
        
        progress_frame = tk.Frame(parent, bg=COLORS['shadow'], bd=2, relief='ridge')
        progress_frame.pack(fill=tk.X, pady=10, padx=50)
        
        tk.Label(progress_frame, text=f"Quest Progress: {completed}/{total} Complete",
                font=('Georgia', 12, 'bold'),
                fg=COLORS['gold'], bg=COLORS['shadow']).pack(pady=5)
        
        # Progress bar
        quest_progress = ttk.Progressbar(progress_frame, length=400,
                                         mode='determinate',
                                         maximum=total)
        quest_progress['value'] = completed
        quest_progress.pack(pady=5)
    
    def refresh_character_encounters(self):
        """Refresh the character cards to show updated quest status"""
        if not self.cards_frame:
            return
        
        # Clear existing cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        
        # Create updated cards
        row, col = 0, 0
        for name, data in self.characters.items():
            card = self.quest_system.enhance_character_card(self.cards_frame, name, data)
            card.grid(row=row, column=col, padx=15, pady=15)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def create_gates_of_truth_section(self, parent):
        """Create the 16 Gates of Truth section"""
        section = tk.Frame(parent, bg=COLORS['shadow'])
        section.pack(fill=tk.X, pady=30, padx=50)
        
        # Main frame
        main_frame = tk.Frame(section, bg=COLORS['gold'], bd=5, relief='ridge')
        main_frame.pack(fill=tk.X, padx=50)
        
        content = tk.Frame(main_frame, bg=COLORS['ebony'], bd=3, relief='sunken')
        content.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Title
        tk.Label(content, text="🔮 THE 16 GATES OF TRUTH 🔮",
                font=('Georgia', 26, 'bold'), fg=COLORS['gold'], bg=COLORS['ebony']).pack(pady=20)
        
        tk.Label(content, text="Unlock All Ave Mujica Songs Through Logical Revelation",
                font=('Georgia', 14, 'italic'), fg=COLORS['periwinkle'], bg=COLORS['ebony']).pack()
        
        # Note about quest rewards
        tk.Label(content, text="✨ Completing character quests unlocks deeper song meanings ✨",
                font=('Georgia', 10, 'italic'), fg=COLORS['terracotta'], bg=COLORS['ebony']).pack(pady=5)
        
        # Quiz interface
        self._create_quiz_interface(content)
    
    def _create_quiz_interface(self, parent):
        """Create quiz interface"""
        quiz_frame = tk.Frame(parent, bg=COLORS['ebony'])
        quiz_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Score display
        score_frame = tk.Frame(quiz_frame, bg=COLORS['ebony'])
        score_frame.pack(fill=tk.X, pady=10)
        
        self.quiz_manager.score_display = tk.Label(score_frame,
            text=f"⚜ Grimoire Progress: {self.quiz_manager.questions_answered}/{self.quiz_manager.total_questions} ⚜",
            font=('Georgia', 12, 'bold'),
            fg=COLORS['gold'],
            bg=COLORS['ebony'])
        self.quiz_manager.score_display.pack(side=tk.LEFT, padx=15)
        
        self.quiz_manager.streak_display = tk.Label(score_frame,
            text=f"🔥 Streak: {self.quiz_manager.correct_streak}",
            font=('Georgia', 12),
            fg=COLORS['terracotta'],
            bg=COLORS['ebony'])
        self.quiz_manager.streak_display.pack(side=tk.RIGHT, padx=15)
        
        # Truth table display
        self.quiz_manager.truth_display = tk.Frame(quiz_frame, bg=COLORS['ebony'])
        self.quiz_manager.truth_display.pack(pady=15, padx=20, fill=tk.X)
        
        # Unlocked songs display
        self.songs_frame = tk.Frame(quiz_frame, bg=COLORS['shadow'], bd=2, relief='ridge')
        self.songs_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(self.songs_frame, text="🎵 UNLOCKED SONGS 🎵",
                font=('Georgia', 14, 'bold'),
                fg=COLORS['gold'], bg=COLORS['shadow']).pack(pady=5)
        
        self.songs_display = tk.Frame(self.songs_frame, bg=COLORS['shadow'])
        self.songs_display.pack(pady=10)
        
        self.update_songs_display()
        
        # Initialize quiz
        self.quiz_manager.new_quiz()
    
    def update_songs_display(self):
        """Update the unlocked songs display"""
        if not hasattr(self, 'songs_display'):
            return
        
        # Clear previous display
        for widget in self.songs_display.winfo_children():
            widget.destroy()
        
        if self.unlocked_songs:
            # Create song cards in a grid
            row, col = 0, 0
            for song in self.unlocked_songs:
                song_card = tk.Frame(self.songs_display, bg=song['color'], bd=2, relief='raised')
                song_card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                
                tk.Label(song_card, text=song['title'],
                        font=('Georgia', 10, 'bold'),
                        fg=COLORS['gold'], bg=song['color']).pack(pady=2)
                
                tk.Label(song_card, text=song['operation'],
                        font=('Georgia', 8),
                        fg=COLORS['cream'], bg=song['color']).pack()
                
                tk.Label(song_card, text=f"\"{song['lyric'][:30]}...\"",
                        font=('Georgia', 7, 'italic'),
                        fg=COLORS['periwinkle'], bg=song['color'],
                        wraplength=150).pack(pady=2)
                
                col += 1
                if col > 2:
                    col = 0
                    row += 1
        else:
            tk.Label(self.songs_display, text="No songs unlocked yet. Complete quests and solve the gates!",
                    font=('Georgia', 10), fg=COLORS['cream'], bg=COLORS['shadow']).pack()
    
    def create_victorian_status(self, parent):
        """Create the status bar"""
        status_bar = tk.Frame(parent, bg=COLORS['deep_red'], height=40)
        status_bar.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        status_bar.grid_propagate(False)
        
        status_center = tk.Frame(status_bar, bg=COLORS['deep_red'])
        status_center.place(relx=0.5, rely=0.5, anchor='center')
        
        time_str = datetime.now().strftime("⚜  %H:%M  ⚜")
        tk.Label(status_center, text=time_str,
                fg=COLORS['gold'], bg=COLORS['deep_red'],
                font=('Georgia', 9, 'bold')).pack(side=tk.LEFT, padx=10)
        
        completed_quests = sum(1 for c in self.quest_system.quest_completed.values() if c)
        unlocked_songs = len(self.unlocked_songs)
        nav_hint = f"Quests: {completed_quests}/5 Complete | Songs: {unlocked_songs}/5 Unlocked"
        
        tk.Label(status_center, text=nav_hint,
                fg=COLORS['periwinkle'], bg=COLORS['deep_red'],
                font=('Georgia', 9, 'italic')).pack(side=tk.LEFT, padx=20)
        
        quotes = [
            "Sixteen gates, sixteen truths...",
            "Each character has a story to tell",
            "Complete quests to unlock deeper meanings",
            "The masquerade of logic never ends",
            "Truth wears many masks"
        ]
        tk.Label(status_center, text=random.choice(quotes),
                fg=COLORS['gold'], bg=COLORS['deep_red'],
                font=('Georgia', 9, 'italic')).pack(side=tk.LEFT, padx=10)
    
    def create_song_cards(self):
        """Update song cards when new songs are unlocked"""
        self.update_songs_display()