# gui_components.py
# Main GUI application class with centered 16 Gates of Truth

import tkinter as tk
from tkinter import ttk, messagebox, font
import random
from datetime import datetime
from PIL import Image, ImageTk
import os

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
    """Manages character data with image filenames"""
    
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
                'image': '🎹',
                'image_file': 'sakiko.png'
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
                'image': '🎸',
                'image_file': 'uika.png'
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
                'image': '🎸',
                'image_file': 'mutsumi.png'
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
                'image': '🎸',
                'image_file': 'umiri.png'
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
                'image': '🥁',
                'image_file': 'nyamu.png'
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
    """Manages logical operations data - UPDATED with all 16 unique operations"""
    
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
    """Manages Ave Mujica songs data - UPDATED with new assignments"""
    def __init__(self):
        self.songs = [
            # Binary Operations
            {
                'title': 'Ave Mujica',
                'operation': 'NAND',
                'meaning': 'The band\'s anthem - not all is as it seems - false only when everything appears true',
                'color': '#5C3A3A',
                'lyric': "We are not merely what you see before you...",
                'image_file': 'avemujica.png'
            },
            {
                'title': 'KiLLKiSS',
                'operation': 'XOR',
                'meaning': 'Kill or kiss - exactly one must be chosen - the ultimate exclusive choice',
                'color': '#8B0000',
                'lyric': "The line between love and death blurs...",
                'image_file': 'killkiss.png'
            },
            {
                'title': 'georgette me, georgette you',
                'operation': 'XNOR',
                'meaning': 'I am you if and only if you are me - perfect mutual identity and reflection',
                'color': '#9E7B9B',
                'lyric': "When I become you and you become me, we are complete...",
                'image_file': 'georgette.png'
            },
            {
                'title': 'Kuro no Birthday',
                'operation': 'OR',
                'meaning': 'Darkness or birth - at least one must be true - duality of existence',
                'color': '#2D1B1B',
                'lyric': "A birthday in darkness, where shadows or light may prevail...",
                'image_file': 'kuronobirthday.png'
            },
            {
                'title': 'Sophie',
                'operation': 'AND',
                'meaning': 'Wisdom requires both knowledge AND understanding - both heart and mind must speak',
                'color': '#9E7B9B',
                'lyric': "In the pursuit of truth, both heart and mind must speak...",
                'image_file': 'sophie.png'
            },
            {
                'title': 'Crucifix X',
                'operation': 'Implication',
                'meaning': 'If you bear the cross, then you must suffer - the promise of sacrifice',
                'color': '#4A2C2C',
                'lyric': "The tenth sacrifice carries the weight of all...",
                'image_file': 'crucifixX.png'
            },
            {
                'title': 'Deep Into The Forest',
                'operation': 'NOR',
                'meaning': 'Neither path leads where you expect - both paths are false',
                'color': '#2C4A2C',
                'lyric': "Lost in the woods where no trail is true...",
                'image_file': 'deepintoforest.png'
            },
            
            # Symbol Series
            {
                'title': 'Symbol I: △ Fire',
                'operation': 'Converse Implication',
                'meaning': 'Fire transforms - if it burns, then it was ignited - reverse cause and effect',
                'color': '#C44C4C',
                'lyric': "The triangle burns with consuming passion...",
                'image_file': 'fire.png'
            },
            {
                'title': 'Symbol II: 🜁 Air',
                'operation': 'Negation of P',
                'meaning': 'Wind carries - denies the expected - invisible forces negate what we know',
                'color': '#6BA5B0',
                'lyric': "Invisible forces guide our fate...",
                'image_file': 'air.png'
            },
            {
                'title': 'Symbol III: ▽ Water',
                'operation': 'Material Nonimplication',
                'meaning': 'Water carves - only when P without Q - flows under specific conditions',
                'color': '#3A6B8C',
                'lyric': "Flowing tears shape the stone of memory...",
                'image_file': 'water.png'
            },
            {
                'title': 'Symbol IV: 🜃 Earth',
                'operation': 'Converse Nonimplication',
                'meaning': 'Earth grounds - only when Q without P - the soil remembers selectively',
                'color': '#6B4C2C',
                'lyric': "The soil remembers what we forget...",
                'image_file': 'earth.png'
            },
            
            # Special Operations
            {
                'title': 'Imprisoned XII',
                'operation': 'Contradiction',
                'meaning': 'Freedom is impossible - always false - eternal confinement',
                'color': '#1A1A1A',
                'lyric': "Twelve chains bind the soul in eternal confinement...",
                'image_file': 'XII.png'
            },
            {
                'title': 'Octagram Dance',
                'operation': 'Tautology',
                'meaning': 'The eight-pointed star dances eternally - always true, always present',
                'color': '#C49A6C',
                'lyric': "Eight points, one circle, all moving as one...",
                'image_file': 'octagramdance.png'
            },
            
            # Projections
            {
                'title': 'DIVINE',
                'operation': 'Projection Q',
                'meaning': 'The gods speak only when we listen - divine truth is projected through faith',
                'color': '#C49A6C',
                'lyric': "The gods speak only when we listen...",
                'image_file': 'divine.png'
            },
            {
                'title': 'Alter Ego',
                'operation': 'Projection P',
                'meaning': 'The mask and the face - true self projects regardless of false self',
                'color': '#8A6E8E',
                'lyric': "The mask and the face cannot both be real...",
                'image_file': 'alterego.png'
            },
            {
                'title': 'Ether',
                'operation': 'Negation of Q',
                'meaning': 'The fifth element negates the other four - beyond the four, the void speaks',
                'color': '#C4A962',
                'lyric': "Beyond the four, the void speaks eternal truths...",
                'image_file': 'ether.png'
            },
        ]
    
    def __getitem__(self, index):
        return self.songs[index]
    
    def __len__(self):
        return len(self.songs)
    
    def __iter__(self):
        return iter(self.songs)


class QuizManager:
    """Manages quiz state and logic - UPDATED for random unique questions"""
    
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
        
        # NEW: Track which operations have been asked
        self.available_operation_indices = list(range(16))  # 0-15 indices
        self.asked_operations = []  # Track asked operations
        self.operation_order = []   # Random order of operations
        
        self.score_display = None
        self.streak_display = None
        self.truth_display = None
        self.operation_label = None
        self.options_frame = None
        self.submit_btn = None
        self.status_icon = None
        self.status_message = None
        self.option_buttons = []
        self.songs_container = None
        self.song_cards = []
        
        # Shuffle operations at start
        self.shuffle_operations()
    
    def shuffle_operations(self):
        """Create a random order of all 16 unique operations"""
        self.available_operation_indices = list(range(16))
        random.shuffle(self.available_operation_indices)
        self.operation_order = self.available_operation_indices.copy()
        self.asked_operations = []
        print(f"Operation order: {self.operation_order}")  # Debug
    
    def new_quiz(self):
        """Start a new quiz round with unique random operation"""
        if self.questions_answered < self.total_questions:
            # Get the next operation from the shuffled list
            if self.available_operation_indices:
                self.current_operation_index = self.available_operation_indices.pop(0)
                self.asked_operations.append(self.current_operation_index)
            else:
                # Fallback if something goes wrong
                self.current_operation_index = random.randint(0, 15)
            
            self.display_current_truth_table()
            self.answer_submitted = False
            
            # Reset button highlights
            for btn_info in self.option_buttons:
                btn_info['button'].config(bg=COLORS['option_button'])
            
            if hasattr(self, 'selected_button'):
                self.selected_button = None
            
            if self.submit_btn:
                self.submit_btn.config(state=tk.DISABLED, bg=COLORS['deep_red'])
            if self.status_icon:
                self.status_icon.config(text="", bg=COLORS['ebony'])
            if self.status_message:
                self.status_message.config(text="", bg=COLORS['ebony'])
    
    def display_current_truth_table(self):
        """Display current truth table"""
        if not hasattr(self, 'truth_display') or not self.truth_display:
            return
        
        # Clear previous display
        for widget in self.truth_display.winfo_children():
            widget.destroy()
        
        op = self.parent.logical_operations[self.current_operation_index]
        self.create_truth_table_simple(self.truth_display, op)
    
    def create_truth_table_simple(self, parent, op):
        """Create truth table with simple labeled display"""
        # Create main frame for truth table
        main_frame = tk.Frame(parent, bg=COLORS['cream'], bd=3, relief='raised')
        main_frame.pack(fill=tk.X, pady=5)
        
        # Title
        title_label = tk.Label(main_frame, text="TRUTH TABLE",
                              font=('Georgia', 14, 'bold'),
                              bg=COLORS['periwinkle'],
                              fg=COLORS['deep_red'],
                              pady=8)
        title_label.pack(fill=tk.X)
        
        # Create inner frame for the table
        table_frame = tk.Frame(main_frame, bg=COLORS['cream'])
        table_frame.pack(pady=10)
        
        # Header row
        tk.Label(table_frame, text="P", font=('Georgia', 11, 'bold'),
                bg=COLORS['periwinkle'], fg=COLORS['deep_red'],
                width=8, height=1, relief='raised').grid(row=0, column=0, padx=2, pady=2)
        tk.Label(table_frame, text="Q", font=('Georgia', 11, 'bold'),
                bg=COLORS['periwinkle'], fg=COLORS['deep_red'],
                width=8, height=1, relief='raised').grid(row=0, column=1, padx=2, pady=2)
        tk.Label(table_frame, text="Result", font=('Georgia', 11, 'bold'),
                bg=COLORS['periwinkle'], fg=COLORS['deep_red'],
                width=10, height=1, relief='raised').grid(row=0, column=2, padx=2, pady=2)
        
        # Data rows
        truth_values = [
            ('F', 'F', op['truth_table'][0]),
            ('F', 'T', op['truth_table'][1]),
            ('T', 'F', op['truth_table'][2]),
            ('T', 'T', op['truth_table'][3])
        ]
        
        for row, (p, q, val) in enumerate(truth_values, start=1):
            result = 'T' if val else 'F'
            result_color = COLORS['success_green'] if val else COLORS['error_red']
            
            tk.Label(table_frame, text=p, font=('Courier New', 15, 'bold'),
                    bg=COLORS['cream'], fg=COLORS['deep_red'],
                    width=12, height=3, relief='sunken').grid(row=row, column=0, padx=2, pady=2)
            tk.Label(table_frame, text=q, font=('Courier New', 15, 'bold'),
                    bg=COLORS['cream'], fg=COLORS['deep_red'],
                    width=12, height=3, relief='sunken').grid(row=row, column=1, padx=2, pady=2)
            tk.Label(table_frame, text=result, font=('Courier New', 15, 'bold'),
                    bg=COLORS['cream'], fg=result_color,
                    width=12, height=3, relief='sunken').grid(row=row, column=2, padx=2, pady=2)
    
    def select_option(self, operation_name):
        """Handle option selection"""
        if not self.answer_submitted:
            # Reset previous selection
            if hasattr(self, 'selected_button') and self.selected_button:
                self.selected_button.config(bg=COLORS['option_button'])
            
            # Find and highlight the selected button
            for btn_info in self.option_buttons:
                if btn_info['name'] == operation_name:
                    self.selected_button = btn_info['button']
                    self.selected_button.config(bg=COLORS['option_selected'])
                    self.selected_answer = operation_name
                    if self.submit_btn:
                        self.submit_btn.config(state=tk.NORMAL)
                    break
    
    def double_click_answer(self, operation_name):
        """Handle double-click answer"""
        if not self.answer_submitted:
            self.select_option(operation_name)
            self.check_answer()
    
    def on_button_leave(self, button):
        """Handle button leave event"""
        if button.cget('bg') != COLORS['success_green'] and button.cget('bg') != COLORS['error_red']:
            button.config(bg=COLORS['option_button'])
    
    def check_answer(self):
        """Check the answer"""
        if self.answer_submitted or not self.selected_answer:
            return
        
        self.answer_submitted = True
        current_op = self.parent.logical_operations[self.current_operation_index]
        
        if self.selected_answer == current_op['name']:
            self.handle_correct_answer(current_op)
        else:
            self.handle_wrong_answer(current_op, self.selected_answer)
        
        if self.score_display:
            self.score_display.config(
                text=f"⚜ Grimoire Progress: {self.questions_answered}/{self.total_questions} ⚜"
            )
        if self.streak_display:
            self.streak_display.config(text=f"🔥 Streak: {self.correct_streak}")
        
        if self.questions_answered < self.total_questions:
            self.parent.root.after(3000, self.new_quiz)
        else:
            if self.submit_btn:
                self.submit_btn.config(state=tk.DISABLED, bg=COLORS['mauve'])
            self.show_completion_message()
    
    def handle_correct_answer(self, current_op):
        """Handle correct answer"""
        self.questions_answered += 1
        self.correct_streak += 1
        
        # Find and unlock the corresponding song
        song = None
        for s in self.parent.ave_mujica_songs:
            if s['operation'] == current_op['name']:
                song = s
                break
        
        if song and song not in self.parent.unlocked_songs:
            self.parent.unlocked_songs.append(song)
            self.parent.update_songs_display()
        
        if self.status_icon:
            self.status_icon.config(text="✓✓✓ VERITAS ✓✓✓", fg=COLORS['correct_gold'], bg=COLORS['ebony'])
        if self.status_message:
            if song:
                # Check if song has deeper meaning from quests
                deeper_meaning = ""
                for character, quest in self.parent.quest_system.quests.items():
                    if hasattr(quest, 'get_finale') and self.parent.quest_system.quest_completed.get(character, False):
                        if song['title'] in str(quest.get_finale()):
                            deeper_meaning = " (Deeper meaning unlocked!)"
                
                self.status_message.config(
                    text=f"✨ Correct! You have unlocked: {song['title']}{deeper_meaning} ✨",
                    fg=COLORS['cream'], bg=COLORS['ebony'])
            else:
                self.status_message.config(
                    text="✨ Correct! You have unlocked a new song! ✨",
                    fg=COLORS['cream'], bg=COLORS['ebony'])
        
        # Highlight the correct answer in green
        for btn_info in self.option_buttons:
            if btn_info['name'] == current_op['name']:
                btn_info['button'].config(bg=COLORS['success_green'])
                break
        
        if self.submit_btn:
            self.submit_btn.config(state=tk.DISABLED, bg=COLORS['mauve'])
    
    def handle_wrong_answer(self, current_op, selected):
        """Handle wrong answer"""
        self.correct_streak = 0
        
        correct_song = None
        for s in self.parent.ave_mujica_songs:
            if s['operation'] == current_op['name']:
                correct_song = s
                break
        
        if self.status_icon:
            self.status_icon.config(text="✗✗✗ FALSITAS ✗✗✗", fg=COLORS['error_red'], bg=COLORS['ebony'])
        if self.status_message:
            if correct_song:
                self.status_message.config(
                    text=f"❌ Incorrect. The correct operation was: {current_op['name']} {current_op['symbol']}\n"
                         f"This would unlock: {correct_song['title']}",
                    fg=COLORS['cream'], bg=COLORS['ebony'])
            else:
                self.status_message.config(
                    text=f"❌ Incorrect. The correct operation was: {current_op['name']} {current_op['symbol']}",
                    fg=COLORS['cream'], bg=COLORS['ebony'])
        
        # Highlight correct answer in green and wrong selection in red
        for btn_info in self.option_buttons:
            if btn_info['name'] == current_op['name']:
                btn_info['button'].config(bg=COLORS['success_green'])
            elif btn_info['name'] == selected:
                btn_info['button'].config(bg=COLORS['error_red'])
        
        if self.submit_btn:
            self.submit_btn.config(state=tk.DISABLED, bg=COLORS['mauve'])
    
    def restart_quiz(self):
        """Restart the quiz with fresh random order"""
        result = messagebox.askyesno(
            "Restart Grimoire",
            "Are you sure you want to restart? All progress will be lost and songs will be locked again."
        )
        
        if result:
            self.questions_answered = 0
            self.correct_streak = 0
            self.parent.unlocked_songs = []
            self.answer_submitted = False
            
            # Reshuffle operations
            self.shuffle_operations()
            
            if self.score_display:
                self.score_display.config(text=f"⚜ Grimoire Progress: 0/{self.total_questions} ⚜")
            if self.streak_display:
                self.streak_display.config(text="🔥 Streak: 0")
            
            # Reset button highlights
            for btn_info in self.option_buttons:
                btn_info['button'].config(bg=COLORS['option_button'])
            
            if hasattr(self, 'selected_button'):
                self.selected_button = None
            
            if self.submit_btn:
                self.submit_btn.config(state=tk.DISABLED, bg=COLORS['deep_red'])
            if self.status_icon:
                self.status_icon.config(text="", bg=COLORS['ebony'])
            if self.status_message:
                self.status_message.config(text="", bg=COLORS['ebony'])
            
            self.parent.update_songs_display()
            self.new_quiz()
            
            messagebox.showinfo("Grimoire Reset", "The gates have closed. Begin your journey anew...")
    
    def show_completion_message(self):
        """Show completion message"""
        if self.status_icon:
            self.status_icon.config(text="🎉 GRIMOIRE COMPLETE 🎉", fg=COLORS['gold'], bg=COLORS['ebony'])
        if self.status_message:
            self.status_message.config(
                text="You have unlocked all 16 songs! The masquerade's secrets are yours.",
                fg=COLORS['cream'], bg=COLORS['ebony'])
        
        # Check if all quests are also completed
        if all(self.parent.quest_system.quest_completed.values()):
            messagebox.showinfo("The Ultimate Truth", 
                              "You have mastered all operations AND completed every character's journey!\n\n"
                              "The full story of Ave Mujica is now yours to understand.")
        else:
            messagebox.showinfo("Grimoire Complete", 
                              "Congratulations! You have unlocked all 16 songs!\n\n"
                              "But the characters still have stories to tell...\n"
                              "Complete their quests to unlock the deepest meanings.")
    
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
        self.root.geometry("1400x1000")
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
        
        # Image storage
        self.intro_image = None
        self.character_images = {}
        self.song_images = {}
        
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
    
    def center_window(self, window, width, height):
        """Center a window on the screen"""
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f'{width}x{height}+{x}+{y}')
    
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
        """Create centered navigation bar with reset button"""
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
        
        # Reset button
        reset_btn = tk.Button(nav_center, text="⟲ Reset",
                             command=self.open_reset_menu,
                             bg=COLORS['error_red'], fg=COLORS['gold'],
                             font=('Georgia', 11, 'bold'), relief='raised',
                             borderwidth=2, padx=20, pady=8, cursor='hand2')
        reset_btn.pack(side=tk.LEFT, padx=10)
    
    def scroll_to_section(self, section_id):
        """Scroll to a specific section"""
        if section_id == 0:  # Intro
            self.canvas.yview_moveto(0)
        elif section_id == 1:  # Truth Cathedral
            self.canvas.yview_moveto(0.2)
        elif section_id == 2:  # Character Encounters
            self.canvas.yview_moveto(0.45)
        elif section_id == 3:  # 16 Gates
            self.canvas.yview_moveto(0.7)
        
    def open_reset_menu(self):
        """Open reset menu"""
        reset_window = tk.Toplevel(self.root)
        reset_window.title("Reset Progress")
        reset_window.configure(bg=COLORS['ebony'])
        reset_window.transient(self.root)
        reset_window.grab_set()
        
        self.window_manager.center_window(reset_window, 500, 400)
        
        # Main frame
        main_frame = tk.Frame(reset_window, bg=COLORS['ebony'], padx=30, pady=30)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title
        tk.Label(main_frame, text="⟲ Reset Options",
                font=('Georgia', 20, 'bold'), fg=COLORS['gold'],
                bg=COLORS['ebony']).pack(pady=20)
        
        # Description
        tk.Label(main_frame, 
                text="Choose what you would like to reset:",
                font=('Georgia', 12), fg=COLORS['cream'],
                bg=COLORS['ebony']).pack(pady=10)
        
        # Reset buttons
        button_frame = tk.Frame(main_frame, bg=COLORS['ebony'])
        button_frame.pack(pady=20)
        
        # Individual character resets
        tk.Label(button_frame, text="Reset Individual Quests:",
                font=('Georgia', 10, 'bold'), fg=COLORS['periwinkle'],
                bg=COLORS['ebony']).pack(pady=5)
        
        char_frame = tk.Frame(button_frame, bg=COLORS['ebony'])
        char_frame.pack(pady=10)
        
        row, col = 0, 0
        for character in self.characters.keys():
            btn = tk.Button(char_frame, text=character.split()[0],
                           command=lambda c=character: self.quest_system.confirm_reset_character(c),
                           bg=COLORS['deep_red'], fg=COLORS['gold'],
                           font=('Georgia', 9, 'bold'),
                           width=12, pady=5, cursor='hand2')
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Separator
        tk.Frame(main_frame, bg=COLORS['gold'], height=2).pack(fill=tk.X, pady=20)
        
        # Reset all button
        tk.Button(main_frame, text="⚠️ RESET ALL PROGRESS ⚠️",
                 command=lambda: [reset_window.destroy(), self.quest_system.confirm_reset_all()],
                 bg=COLORS['error_red'], fg=COLORS['gold'],
                 font=('Georgia', 12, 'bold'), relief='raised',
                 borderwidth=3, padx=30, pady=10, cursor='hand2').pack(pady=10)
        
        # Warning
        tk.Label(main_frame, 
                text="Warning: Resetting progress cannot be undone!",
                font=('Georgia', 9, 'italic'), fg=COLORS['terracotta'],
                bg=COLORS['ebony']).pack(pady=10)
        
        # Close button
        tk.Button(main_frame, text="Cancel",
                 command=reset_window.destroy,
                 bg=COLORS['shadow'], fg=COLORS['cream'],
                 font=('Georgia', 10), cursor='hand2').pack(pady=10)
    
    def open_quest_hub(self):
        """Open the quest selection hub"""
        quest_hub = tk.Toplevel(self.root)
        quest_hub.title("Ave Mujica - Character Quests")
        quest_hub.configure(bg=COLORS['ebony'])
        quest_hub.transient(self.root)
        quest_hub.grab_set()
        
        self.center_window(quest_hub, 1000, 800)
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
        """Create the intro section with an image banner"""
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
        
        # ADD IMAGE HERE - before the welcome text
        image_frame = tk.Frame(content, bg=COLORS['ebony'])
        image_frame.pack(pady=20)
        
        # Try to load and display the intro image
        image_path = 'assets/images/intro_banner.png'
        if os.path.exists(image_path):
            try:
                # Load and resize image
                pil_image = Image.open(image_path)
                # Resize to fit (adjust dimensions as needed)
                pil_image = pil_image.resize((650, 822), Image.Resampling.LANCZOS)
                self.intro_image = ImageTk.PhotoImage(pil_image)  # Keep reference
                
                # Display image
                image_label = tk.Label(image_frame, image=self.intro_image, bg=COLORS['ebony'])
                image_label.pack()
            except Exception as e:
                print(f"Could not load intro image: {e}")
                # Fallback to text if image fails
                tk.Label(image_frame, text="[AVE MUJICA BANNER]", 
                        font=('Georgia', 20, 'bold'), fg=COLORS['gold'], 
                        bg=COLORS['ebony']).pack()
        else:
            # Fallback if image doesn't exist
            tk.Label(image_frame, text="[AVE MUJICA BANNER]", 
                    font=('Georgia', 20, 'bold'), fg=COLORS['gold'], 
                    bg=COLORS['ebony']).pack()
            print(f"Image not found: {image_path}")
        
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
        
        self.center_window(tutorial_window, 900, 800)
        
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
        if not hasattr(self, 'cards_frame') or self.cards_frame is None:
            print("Warning: cards_frame not initialized yet")
            return
        
        try:
            if not self.cards_frame.winfo_exists():
                print("Warning: cards_frame no longer exists")
                return
        except:
            print("Warning: cards_frame is invalid")
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
        
        self.cards_frame.update_idletasks()
    
    def create_gates_of_truth_section(self, parent):
        """Create the 16 Gates of Truth section with centered quiz interface"""
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
        
        # Add note about quest rewards
        tk.Label(content, text="✨ Completing character quests unlocks deeper song meanings ✨",
                font=('Georgia', 10, 'italic'), fg=COLORS['terracotta'], bg=COLORS['ebony']).pack(pady=5)
        
        # Quiz interface
        quiz_frame = tk.Frame(content, bg=COLORS['ebony'])
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
        
        # Question
        self.quiz_manager.question_label = tk.Label(quiz_frame,
            text="Which logical operation produces this truth table?",
            font=('Georgia', 14),
            fg=COLORS['periwinkle'],
            bg=COLORS['ebony'])
        self.quiz_manager.question_label.pack(pady=10)
        
        # Click instruction
        tk.Label(quiz_frame,
            text="(Click any button to select and lock in your guess)",
            font=('Georgia', 10, 'italic'),
            fg=COLORS['gold'],
            bg=COLORS['ebony']).pack()
        
        # Status display
        self.quiz_manager.status_frame = tk.Frame(quiz_frame, bg=COLORS['ebony'], height=60)
        self.quiz_manager.status_frame.pack(fill=tk.X, pady=5)
        
        self.quiz_manager.status_icon = tk.Label(self.quiz_manager.status_frame,
            text="",
            font=('Georgia', 20),
            bg=COLORS['ebony'])
        self.quiz_manager.status_icon.pack()
        
        self.quiz_manager.status_message = tk.Label(self.quiz_manager.status_frame,
            text="",
            font=('Georgia', 11, 'italic'),
            bg=COLORS['ebony'],
            wraplength=600)
        self.quiz_manager.status_message.pack()
        
        # Operation selection area - Buttons grid (4x4)
        options_frame = tk.Frame(quiz_frame, bg=COLORS['ebony'])
        options_frame.pack(pady=15, fill=tk.X)
        
        # Center the options grid
        options_center = tk.Frame(options_frame, bg=COLORS['ebony'])
        options_center.pack(expand=True)
        
        # Create a grid frame for the option buttons
        self.quiz_manager.option_buttons_grid = tk.Frame(options_center, bg=COLORS['ebony'])
        self.quiz_manager.option_buttons_grid.pack()
        
        # Operation selection variable
        self.quiz_manager.operation_var = tk.StringVar()
        self.quiz_manager.option_buttons = []
        
        # Create operation buttons in a 4x4 grid
        for i, op in enumerate(self.logical_operations):
            row = i // 4
            col = i % 4
            
            # Create a frame for each button with padding
            btn_frame = tk.Frame(self.quiz_manager.option_buttons_grid, bg=COLORS['ebony'])
            btn_frame.grid(row=row, column=col, padx=8, pady=8)
            
            # Create button with operation name and symbol
            btn_text = f"{op['symbol']}\n{op['name']}"
            btn = tk.Button(btn_frame,
                text=btn_text,
                bg=COLORS['option_button'],
                fg=COLORS['cream'],
                font=('Georgia', 9, 'bold'),
                relief='raised',
                borderwidth=3,
                width=25,
                height=3,
                cursor='hand2',
                command=lambda op_name=op['name']: self.quiz_manager.select_option(op_name))
            
            # Bind double-click
            btn.bind('<Double-Button-1>', lambda e, op_name=op['name']: self.quiz_manager.double_click_answer(op_name))
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS['option_hover']))
            btn.bind("<Leave>", lambda e, b=btn: self.quiz_manager.on_button_leave(b))
            
            btn.pack()
            
            # Store button reference
            self.quiz_manager.option_buttons.append({
                'button': btn,
                'frame': btn_frame,
                'name': op['name'],
                'original_bg': COLORS['option_button']
            })
        
        # Submit button
        button_frame = tk.Frame(quiz_frame, bg=COLORS['ebony'])
        button_frame.pack(pady=15)
        
        self.quiz_manager.submit_btn = tk.Button(button_frame,
            text="⚜  LOCK IN GUESS (CLICK / DOUBLE-CLICK)  ⚜",
            command=self.quiz_manager.check_answer,
            bg=COLORS['deep_red'],
            fg=COLORS['gold'],
            font=('Georgia', 12, 'bold'),
            relief='raised',
            borderwidth=4,
            padx=30,
            pady=8,
            cursor='hand2',
            state=tk.DISABLED)
        self.quiz_manager.submit_btn.pack()
        
        self.quiz_manager.submit_btn.bind("<Enter>", lambda e: self.quiz_manager.submit_btn.config(bg=COLORS['button_hover']))
        self.quiz_manager.submit_btn.bind("<Leave>", lambda e: self.quiz_manager.submit_btn.config(bg=COLORS['deep_red']))
        
        hints_frame = tk.Frame(quiz_frame, bg=COLORS['ebony'])
        hints_frame.pack(pady=5)
        
        tk.Label(hints_frame,
            text="⚡ Click to select | ⚡ Double-click to select and submit | ⌨️ Press ENTER after selection",
            font=('Georgia', 9, 'italic'),
            fg=COLORS['periwinkle'],
            bg=COLORS['ebony']).pack()
        
        self.quiz_manager.restart_btn = tk.Button(quiz_frame,
            text="🔄  Restart Grimoire  🔄",
            command=self.quiz_manager.restart_quiz,
            bg=COLORS['mauve'],
            fg=COLORS['gold'],
            font=('Georgia', 10),
            relief='raised',
            borderwidth=2,
            padx=20,
            pady=5,
            cursor='hand2')
        self.quiz_manager.restart_btn.pack(pady=10)
        
        self.create_grimoire_display(quiz_frame)
        self.quiz_manager.new_quiz()
    
    def create_grimoire_display(self, parent):
        """Create the grimoire display for unlocked songs"""
        grimoire_frame = tk.LabelFrame(parent, text="❖ Unlocked Songs ❖",
                                      bg=COLORS['ebony'], fg=COLORS['gold'],
                                      font=('Georgia', 10, 'bold'))
        grimoire_frame.pack(fill=tk.X, pady=10, padx=20)
        
        cards_center = tk.Frame(grimoire_frame, bg=COLORS['ebony'])
        cards_center.pack(expand=True)
        
        self.quiz_manager.songs_container = tk.Frame(cards_center, bg=COLORS['ebony'])
        self.quiz_manager.songs_container.pack(fill=tk.X, pady=5)
        
        self.update_songs_display()
    
    def update_songs_display(self):
        """Update the unlocked songs display with full song information"""
        if not hasattr(self.quiz_manager, 'songs_container') or not self.quiz_manager.songs_container:
            return
        
        # Clear previous display
        for widget in self.quiz_manager.songs_container.winfo_children():
            widget.destroy()
        
        # Center the cards grid
        cards_grid = tk.Frame(self.quiz_manager.songs_container, bg=COLORS['ebony'])
        cards_grid.pack(expand=True)
        
        # Create cards in a grid (4 per row)
        row_frame = None
        for i, song in enumerate(self.ave_mujica_songs[:16]):
            if i % 4 == 0:
                row_frame = tk.Frame(cards_grid, bg=COLORS['ebony'])
                row_frame.pack(fill=tk.X, pady=2)
            
            locked = song not in self.unlocked_songs

            # Create card
            card = tk.Frame(row_frame, bg=COLORS['deep_red'] if locked else song['color'],
                          bd=2, relief='raised', width=250, height=550)
            card.pack(side=tk.LEFT, padx=4, pady=4)
            card.pack_propagate(False)
            
            inner = tk.Frame(card, bg=COLORS['ebony'], bd=1, relief='sunken')
            inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            
            if locked:
                # LOCKED - Show lock icon and placeholder
                tk.Label(inner, text="🔒", 
                        font=('Georgia', 24), bg=COLORS['ebony'],
                        fg=COLORS['deep_red']).pack(pady=(20, 5))
                tk.Label(inner, text="???", 
                        font=('Georgia', 15, 'bold'), bg=COLORS['ebony'],
                        fg=COLORS['cream']).pack()
                tk.Label(inner, text="Locked", 
                        font=('Georgia', 15, 'italic'), bg=COLORS['ebony'],
                        fg=COLORS['periwinkle']).pack()
            else:
                # UNLOCKED - Try to show image, fallback to text
                image_path = f'assets/images/songs/{song["image_file"]}'
                
                if os.path.exists(image_path):
                    try:
                        # Load and resize image
                        pil_image = Image.open(image_path)
                        pil_image = pil_image.resize((220, 180), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(pil_image)
                        
                        # Store reference
                        if not hasattr(self, 'song_images'):
                            self.song_images = {}
                        self.song_images[song['title']] = photo
                        
                        # Display image
                        img_label = tk.Label(inner, image=photo, bg=COLORS['ebony'])
                        img_label.pack(pady=(5, 2))
                        
                    except Exception as e:
                        print(f"Could not load image for {song['title']}: {e}")
                        # Show text placeholder if image fails
                        tk.Label(inner, text="[NO IMAGE]", 
                                font=('Georgia', 20, 'bold'), bg=COLORS['ebony'],
                                fg=COLORS['gold']).pack(pady=(20, 5))
                else:
                    # No image file, show text placeholder
                    print(f"Image not found: {image_path}")
                    tk.Label(inner, text="[NO IMAGE]", 
                            font=('Georgia', 20, 'bold'), bg=COLORS['ebony'],
                            fg=COLORS['gold']).pack(pady=(20, 5))
                
                # SONG TITLE
                title_label = tk.Label(inner, text=song['title'],
                                      font=('Georgia', 20, 'bold'), bg=COLORS['ebony'],
                                      fg=COLORS['gold'], wraplength=180, justify=tk.CENTER)
                title_label.pack(pady=(2, 1))
                
                # OPERATION
                tk.Label(inner, text=f"({song['operation']})",
                        font=('Georgia', 11, 'italic'), bg=COLORS['ebony'],
                        fg=COLORS['periwinkle']).pack(pady=(0, 2))
                
                # MEANING
                meaning_text = song['meaning'][:85] + "..." if len(song['meaning']) > 85 else song['meaning']
                tk.Label(inner, text=meaning_text,
                        font=('Georgia', 15), bg=COLORS['ebony'],
                        fg=COLORS['cream'], wraplength=180, justify=tk.CENTER).pack(pady=(1, 1))
                
                # LYRIC
                lyric_text = song['lyric'][:80] + "..." if len(song['lyric']) > 80 else song['lyric']
                tk.Label(inner, text=f"\"{lyric_text}\"",
                        font=('Georgia', 15, 'italic'), bg=COLORS['ebony'],
                        fg=COLORS['periwinkle'], wraplength=180, justify=tk.CENTER).pack(pady=(1, 3))

    def _show_song_text_fallback(self, parent, song):
        """Show text-based song display with full information when image is not available"""
        # SONG TITLE
        title_label = tk.Label(parent, text=song['title'],
                              font=('Georgia', 10, 'bold'), bg=COLORS['ebony'],
                              fg=COLORS['gold'], wraplength=180, justify=tk.CENTER)
        title_label.pack(pady=(10, 1))
        
        # OPERATION
        tk.Label(parent, text=f"({song['operation']})",
                font=('Georgia', 8, 'italic'), bg=COLORS['ebony'],
                fg=COLORS['periwinkle']).pack(pady=(0, 3))
        
        # MEANING
        meaning_text = song['meaning'][:45] + "..." if len(song['meaning']) > 45 else song['meaning']
        tk.Label(parent, text=meaning_text,
                font=('Georgia', 6), bg=COLORS['ebony'],
                fg=COLORS['cream'], wraplength=180, justify=tk.CENTER).pack(pady=(2, 2))
        
        # LYRIC
        lyric_text = song['lyric'][:40] + "..." if len(song['lyric']) > 40 else song['lyric']
        tk.Label(parent, text=f"\"{lyric_text}\"",
                font=('Georgia', 5, 'italic'), bg=COLORS['ebony'],
                fg=COLORS['periwinkle'], wraplength=180, justify=tk.CENTER).pack(pady=(2, 5))

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
        nav_hint = f"Quests: {completed_quests}/5 Complete | Songs: {unlocked_songs}/16 Unlocked"
        
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