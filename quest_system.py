# quest_system.py
# Character Quest System with improved architecture and reset functionality

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import json
import os
from PIL import Image, ImageTk  # Added for image support

from config import COLORS


class QuestStatus(Enum):
    """Quest status enumeration"""
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class QuestStatusInfo:
    """Data class for quest status information"""
    status: QuestStatus
    color: str
    display_text: str
    icon: str
    progress_text: str
    progress_value: Optional[int] = None
    progress_max: Optional[int] = None


class WindowManager:
    """Manages window creation and centering"""
    
    @staticmethod
    def center_window(window: tk.Toplevel, width: int, height: int) -> None:
        """Center a window on the screen"""
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    @staticmethod
    def position_window_on_side(window: tk.Toplevel, parent_window: tk.Tk, width: int, height: int, side: str = 'right') -> None:
        """Position window on a specific side of the main window"""
        window.update_idletasks()
        
        # Get main window position and size
        main_x = parent_window.winfo_x()
        main_y = parent_window.winfo_y()
        main_width = parent_window.winfo_width()
        main_height = parent_window.winfo_height()
        
        # Ensure main window dimensions are valid
        if main_width < 100:
            main_width = 1400
        if main_height < 100:
            main_height = 900
        
        if side == 'right':
            x = main_x + main_width + 5
            y = main_y + max(0, (main_height - height) // 2)
        elif side == 'left':
            x = max(0, main_x - width - 5)
            y = main_y + max(0, (main_height - height) // 2)
        elif side == 'top':
            x = main_x + max(0, (main_width - width) // 2)
            y = max(0, main_y - height - 5)
        elif side == 'bottom':
            x = main_x + max(0, (main_width - width) // 2)
            y = main_y + main_height + 5
        else:  # center
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
        
        # Ensure window stays on screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))
        
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    @staticmethod
    def create_scrollable_frame(parent: tk.Widget, bg_color: str) -> tuple:
        """Create a scrollable frame with canvas and scrollbar"""
        container = tk.Frame(parent, bg=bg_color)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container, bg=bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollable = tk.Frame(canvas, bg=bg_color)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Bind mousewheel for scrolling (Windows/Mac) - with safety check
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        # Linux scroll bindings - with safety check
        def _on_scroll_up(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(-3, "units")
            except:
                pass
        
        def _on_scroll_down(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(3, "units")
            except:
                pass
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", _on_scroll_up)
        canvas.bind("<Button-5>", _on_scroll_down)
        
        # Also bind to scrollable frame
        scrollable.bind("<Button-4>", _on_scroll_up)
        scrollable.bind("<Button-5>", _on_scroll_down)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        return scrollable, canvas
    
    @staticmethod
    def create_header(parent: tk.Widget, title: str, subtitle: str = "", 
                     bg_color: str = COLORS['ebony']) -> tk.Frame:
        """Create a centered header with decorative elements"""
        header_frame = tk.Frame(parent, bg=bg_color)
        header_frame.pack(fill=tk.X, pady=20)
        
        # Top separator
        top_sep = tk.Frame(header_frame, bg=COLORS['gold'], height=2)
        top_sep.pack(fill=tk.X, pady=(0, 5))
        
        # Title line with decorative dashes
        title_line = tk.Frame(header_frame, bg=bg_color)
        title_line.pack()
        
        tk.Label(title_line, text="⚜", font=('Georgia', 20), 
                fg=COLORS['gold'], bg=bg_color).pack(side=tk.LEFT, padx=10)
        
        tk.Label(title_line, text=title, font=('Georgia', 24, 'bold'),
                fg=COLORS['gold'], bg=bg_color).pack(side=tk.LEFT, padx=10)
        
        tk.Label(title_line, text="⚜", font=('Georgia', 20), 
                fg=COLORS['gold'], bg=bg_color).pack(side=tk.LEFT, padx=10)
        
        # Bottom separator
        bottom_sep = tk.Frame(header_frame, bg=COLORS['gold'], height=2)
        bottom_sep.pack(fill=tk.X, pady=(5, 0))
        
        # Subtitle if provided
        if subtitle:
            tk.Label(header_frame, text=subtitle, font=('Georgia', 12, 'italic'),
                    fg=COLORS['periwinkle'], bg=bg_color).pack(pady=10)
        
        return header_frame


class UIBuilder:
    """Helper class for building consistent UI elements"""
    
    @staticmethod
    def create_dialogue_box(parent: tk.Widget, text: str, height: int = 25) -> tk.Frame:
        """Create a styled dialogue box with scrollable content and larger default height"""
        frame = tk.Frame(parent, bg=COLORS['cream'], bd=3, relief='raised')
        frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(frame, bg=COLORS['cream'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontal scrollbar for long lines
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        text_widget = tk.Text(text_frame, height=height, bg=COLORS['cream'], 
                              fg=COLORS['deep_red'], font=('Georgia', 12), 
                              wrap=tk.WORD, padx=25, pady=25,
                              yscrollcommand=v_scrollbar.set,
                              xscrollcommand=h_scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)
        
        v_scrollbar.config(command=text_widget.yview)
        h_scrollbar.config(command=text_widget.xview)
        
        return frame
    
    @staticmethod
    def create_challenge_box(parent: tk.Widget, challenge: str) -> tk.Frame:
        """Create a styled challenge box"""
        frame = tk.Frame(parent, bg=COLORS['shadow'], bd=2, relief='ridge')
        frame.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(frame, text="⚔ CHALLENGE ⚔", font=('Georgia', 12, 'bold'),
                fg=COLORS['gold'], bg=COLORS['shadow']).pack(pady=5)
        
        tk.Label(frame, text=challenge, font=('Georgia', 10),
                fg=COLORS['cream'], bg=COLORS['shadow'],
                wraplength=700, justify=tk.CENTER).pack(pady=5, padx=20)
        
        return frame
    
    @staticmethod
    def create_scene_indicator(parent: tk.Widget, scene: str) -> tk.Frame:
        """Create a scene location indicator"""
        frame = tk.Frame(parent, bg=COLORS['shadow'], bd=1, relief='sunken')
        frame.pack(fill=tk.X, pady=5, padx=20)
        
        tk.Label(frame, text=f"📍 {scene.replace('_', ' ').title()}",
                font=('Georgia', 9, 'italic'),
                fg=COLORS['periwinkle'], bg=COLORS['shadow']).pack(pady=2)
        
        return frame
    
    @staticmethod
    def create_progress_bar(parent: tk.Widget, current: int, maximum: int, 
                           text: str = "Quest Progress") -> tk.Frame:
        """Create a progress bar with label"""
        frame = tk.Frame(parent, bg=COLORS['ebony'])
        frame.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(frame, text=f"{text}: Stage {current}/{maximum}",
                font=('Georgia', 10, 'bold'),
                fg=COLORS['gold'], bg=COLORS['ebony']).pack()
        
        progress_bar = ttk.Progressbar(frame, length=400, mode='determinate', maximum=maximum)
        progress_bar['value'] = current
        progress_bar.pack(pady=5)
        
        return frame
    
    @staticmethod
    def create_button(parent: tk.Widget, text: str, command: Callable,
                     bg_color: str = COLORS['deep_red'], 
                     fg_color: str = COLORS['gold'],
                     font_size: int = 11, bold: bool = True,
                     padx: int = 20, pady: int = 5) -> tk.Button:
        """Create a styled button"""
        font_spec = ('Georgia', font_size, 'bold') if bold else ('Georgia', font_size)
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=bg_color, fg=fg_color, font=font_spec,
                       relief='raised', borderwidth=2,
                       padx=padx, pady=pady, cursor='hand2')
        btn.pack(pady=10)
        
        return btn


class PuzzleManager:
    """Manages puzzle creation and validation"""
    
    def __init__(self):
        self.answers = []
        self.expected = []
        self.lessons = []
        self.lesson_label = None
        self.payoff_label = None
        self.complete_btn = None
        self.puzzle_lesson = ""
        self.complete_callback = None
        self.stage_complete = False
    
    def create_truth_table_puzzle(self, parent: tk.Widget, puzzle_data: List[Dict], 
                                  lesson: str, complete_callback: Callable) -> None:
        """Create an improved interactive truth table puzzle with larger display"""
        self.puzzle_lesson = lesson
        self.answers = []
        self.expected = []
        self.lessons = []
        self.complete_callback = complete_callback
        self.stage_complete = False
        
        # Centered container
        container = tk.Frame(parent, bg=COLORS['cream'])
        container.pack(expand=True)
        
        # Calculate max text length for dynamic sizing
        max_text_length = 0
        for data in puzzle_data:
            max_text_length = max(max_text_length, len(str(data['P'])), len(str(data['Q'])))
        
        # Set cell width based on content - LARGER
        cell_width = min(30, max(15, max_text_length + 8))
        
        # Table wrapper frame
        table_wrapper = tk.Frame(container, bg=COLORS['gold'], bd=3, relief='ridge')
        table_wrapper.pack(pady=15, padx=10)
        
        # Inner table frame
        table_frame = tk.Frame(table_wrapper, bg=COLORS['cream'])
        table_frame.pack(pady=10, padx=10)
        
        # Table headers - LARGER
        headers = ['P (Premise)', 'Q (Conclusion)', 'Your Answer (T/F)']
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, font=('Georgia', 12, 'bold'),
                           bg=COLORS['wine'], fg=COLORS['cream'],
                           relief='raised', borderwidth=3, 
                           width=max(15, cell_width), height=2)
            label.grid(row=0, column=i, padx=3, pady=3)
        
        # Interactive rows - LARGER
        for row, data in enumerate(puzzle_data, start=1):
            # P value
            p_label = tk.Label(table_frame, text=str(data['P']), 
                              font=('Georgia', 11),
                              bg=COLORS['cream'], fg=COLORS['deep_red'], 
                              width=max(15, cell_width), height=3,
                              relief='sunken', borderwidth=2,
                              wraplength=max(150, cell_width * 6), anchor='center')
            p_label.grid(row=row, column=0, padx=3, pady=3)
            
            # Q value
            q_label = tk.Label(table_frame, text=str(data['Q']), 
                              font=('Georgia', 11),
                              bg=COLORS['cream'], fg=COLORS['deep_red'], 
                              width=max(15, cell_width), height=3,
                              relief='sunken', borderwidth=2,
                              wraplength=max(150, cell_width * 6), anchor='center')
            q_label.grid(row=row, column=1, padx=3, pady=3)
            
            # Answer entry
            answer_var = tk.StringVar()
            entry = tk.Entry(table_frame, textvariable=answer_var, 
                            width=10, justify='center',
                            font=('Georgia', 14, 'bold'), 
                            bg=COLORS['periwinkle'], fg=COLORS['ebony'],
                            relief='sunken', borderwidth=2)
            entry.grid(row=row, column=2, padx=3, pady=3)
            
            self.answers.append(answer_var)
            self.expected.append(data['expected'])
            self.lessons.append(data.get('lesson', ''))
        
        # Button container
        btn_container = tk.Frame(container, bg=COLORS['cream'])
        btn_container.pack(pady=15)
        
        # Check button
        check_btn = tk.Button(btn_container, text="✓ CHECK ANSWERS",
                             command=self._check_answers,
                             bg=COLORS['crimson'], fg=COLORS['gold'],
                             font=('Georgia', 13, 'bold'), 
                             relief='raised', borderwidth=3,
                             padx=30, pady=10, cursor='hand2')
        check_btn.pack(pady=5)
        
        # Complete button (initially disabled)
        self.complete_btn = tk.Button(btn_container, text="✨ COMPLETE STAGE ✨",
                                      command=self._complete_stage,
                                      bg=COLORS['success_green'], fg=COLORS['gold'],
                                      font=('Georgia', 14, 'bold'), state='disabled',
                                      relief='raised', borderwidth=3,
                                      padx=35, pady=12, cursor='hand2')
        self.complete_btn.pack(pady=5)
        
        # Feedback labels container
        feedback = tk.Frame(container, bg=COLORS['ebony'], bd=2, relief='ridge')
        feedback.pack(fill=tk.X, padx=20, pady=10)
        
        # Lesson label
        self.lesson_label = tk.Label(feedback, text="",
                                     font=('Georgia', 12, 'italic'),
                                     fg=COLORS['periwinkle'], bg=COLORS['ebony'],
                                     wraplength=800, justify=tk.CENTER, pady=10)
        self.lesson_label.pack(fill=tk.X, padx=10)
        
        # Payoff label
        self.payoff_label = tk.Label(feedback, text="",
                                     font=('Georgia', 12, 'italic'),
                                     fg=COLORS['gold'], bg=COLORS['ebony'],
                                     wraplength=800, justify=tk.CENTER, pady=10)
        self.payoff_label.pack(fill=tk.X, padx=10)
    
    def _check_answers(self) -> None:
        """Check puzzle answers and provide feedback"""
        if self.stage_complete:
            return
            
        correct = 0
        for i, (answer, expected) in enumerate(zip(self.answers, self.expected)):
            if answer.get().upper() == expected:
                correct += 1
        
        if correct == len(self.answers):
            self.lesson_label.config(text="✓ Perfect! " + self.puzzle_lesson)
            self.payoff_label.config(text="✨ The truth resonates with your soul... ✨")
            self.complete_btn.config(state='normal')
            self.stage_complete = True
        else:
            self.lesson_label.config(text=f"✗ You got {correct}/{len(self.answers)} correct. Try again!")
            self.payoff_label.config(text="")
    
    def _complete_stage(self) -> None:
        """Complete the stage and trigger callback"""
        if self.complete_callback and self.stage_complete:
            self.complete_callback()


class CharacterQuestSystem:
    """Manages all character quests with improved architecture and reset functionality"""
    
    def __init__(self, parent):
        self.parent = parent
        self.quests: Dict[str, Any] = {}
        self.final_quest = None
        self.completed_quests: List[str] = []
        self.quest_progress: Dict[str, int] = {}
        self.quest_completed: Dict[str, bool] = {}
        self.active_quest = None
        self.active_quest_window = None
        self.window_manager = WindowManager()
        self.ui_builder = UIBuilder()
        self.puzzle_manager = PuzzleManager()
        self.final_shown = False
        self.progress_file = "quest_progress.json"
        self.window_side = 'right'
        self.character_images = {}  # Store character image references
    
    def set_quests(self, quests_dict: Dict[str, Any], final_quest) -> None:
        """Set the quests after imports"""
        self.quests = quests_dict
        self.final_quest = final_quest
        self.quest_progress = {name: 0 for name in self.quests.keys()}
        self.quest_completed = {name: False for name in self.quests.keys()}
        # Always start fresh - delete progress file
        if os.path.exists(self.progress_file):
            try:
                os.remove(self.progress_file)
                print("Previous progress file deleted - starting fresh")
            except:
                pass
        self.load_progress()
    
    def set_window_position(self, side: str) -> None:
        """Set the preferred window position for quest popups"""
        valid_sides = ['left', 'right', 'top', 'bottom', 'center']
        if side in valid_sides:
            self.window_side = side
    
    def get_quest_status(self, character: str) -> QuestStatusInfo:
        """Get the status of a character's quest with detailed info"""
        quest_obj = self.quests[character]
        
        # Get the current stage from the quest object if available
        current_stage = self.quest_progress[character]
        if hasattr(quest_obj, 'current_stage') and quest_obj.current_stage > current_stage:
            # Sync the progress with the quest object
            self.quest_progress[character] = quest_obj.current_stage
            current_stage = quest_obj.current_stage
        
        if self.quest_completed[character]:
            return QuestStatusInfo(
                status=QuestStatus.COMPLETED,
                color=COLORS['success_green'],
                display_text='✓ COMPLETED',
                icon='✨',
                progress_text=f"Mastered {quest_obj.operation}"
            )
        elif current_stage > 0:
            total = quest_obj.stage_count
            return QuestStatusInfo(
                status=QuestStatus.IN_PROGRESS,
                color=COLORS['gold'],
                display_text='⚜ IN PROGRESS',
                icon='🔮',
                progress_text=f"Stage {current_stage}/{total}",
                progress_value=current_stage,
                progress_max=total
            )
        else:
            return QuestStatusInfo(
                status=QuestStatus.AVAILABLE,
                color=COLORS['periwinkle'],
                display_text='🔓 AVAILABLE',
                icon='📖',
                progress_text="Click to begin"
            )
    
    def enhance_character_card(self, parent_frame: tk.Widget, character: str, 
                               data: Dict) -> tk.Frame:
        """Create an enhanced character card with quest integration"""
        status_info = self.get_quest_status(character)
        quest = self.quests[character]
        
        # Create main card frame
        card = tk.Frame(parent_frame, bg=data['color'], bd=4, relief='raised')
        
        # Status banner
        status_frame = tk.Frame(card, bg=status_info.color)
        status_frame.pack(fill=tk.X)
        
        tk.Label(status_frame, text=f"{status_info.icon} {status_info.display_text}",
                font=('Georgia', 8, 'bold'), fg=COLORS['ebony'], 
                bg=status_info.color).pack()
        
        # Main content
        inner = tk.Frame(card, bg=COLORS['ebony'], bd=2, relief='sunken')
        inner.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Character elements
        self._add_character_card_elements(inner, character, data, quest, status_info)
        
        return card
    
    def _add_character_card_elements(self, parent: tk.Widget, character: str,
                                     data: Dict, quest, status_info: QuestStatusInfo) -> None:
        """Add elements to character card with image support"""
        
        # IMAGE - Try to load character image, fallback to emoji
        image_path = f'assets/images/{data["image_file"]}'
        print(f"Looking for image: {image_path}")  # Debug line
        
        if os.path.exists(image_path):
            try:
                # Load and resize image
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((333, 549), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(pil_image)
                
                # Store reference to prevent garbage collection
                if not hasattr(self, 'character_images'):
                    self.character_images = {}
                self.character_images[character] = photo
                
                # Display image
                image_label = tk.Label(parent, image=photo, bg=COLORS['ebony'])
                image_label.pack(pady=(10, 5))
                print(f"Successfully loaded image for {character}")
                
            except Exception as e:
                print(f"Could not load image for {character}: {e}")
                # Fallback to emoji
                tk.Label(parent, text=data['image'], font=('Georgia', 32),
                        bg=COLORS['ebony'], fg=data['color']).pack(pady=(10, 5))
        else:
            # Fallback to emoji if image doesn't exist
            print(f"Image not found: {image_path}")
            tk.Label(parent, text=data['image'], font=('Georgia', 32),
                    bg=COLORS['ebony'], fg=data['color']).pack(pady=(10, 5))
        
        # Name
        tk.Label(parent, text=character, font=('Georgia', 12, 'bold'),
                fg=COLORS['gold'], bg=COLORS['ebony']).pack()
        
        # Role
        tk.Label(parent, text=data['role'], font=('Georgia', 10, 'italic'),
                fg=COLORS['periwinkle'], bg=COLORS['ebony']).pack()
        
        # Instrument
        tk.Label(parent, text=data['instrument'], font=('Georgia', 9),
                fg=COLORS['cream'], bg=COLORS['ebony']).pack()
        
        # Operation
        op_frame = tk.Frame(parent, bg=COLORS['ebony'])
        op_frame.pack(pady=5)
        
        tk.Label(op_frame, text=quest.operation, font=('Georgia', 9, 'bold'),
                fg=COLORS['gold'], bg=COLORS['ebony']).pack(side=tk.LEFT, padx=2)
        
        tk.Label(op_frame, text=quest.symbol, font=('Georgia', 12, 'bold'),
                fg=data['color'], bg=COLORS['ebony']).pack(side=tk.LEFT, padx=2)
        
        # Quest name
        tk.Label(parent, text=quest.quest_name, font=('Georgia', 9, 'italic'),
                fg=COLORS['terracotta'], bg=COLORS['ebony']).pack()
        
        # Progress
        tk.Label(parent, text=status_info.progress_text, font=('Georgia', 8),
                fg=status_info.color, bg=COLORS['ebony']).pack(pady=5)
        
        # Quote
        quote_frame = tk.Frame(parent, bg=COLORS['ebony'])
        quote_frame.pack(pady=5, padx=5, fill=tk.X)
        
        tk.Label(quote_frame, text=f"\"{data['quote']}\"", font=('Georgia', 8, 'italic'),
                fg=COLORS['cream'], bg=COLORS['ebony'], wraplength=180,
                justify=tk.CENTER).pack()
        
        # Button frame with quest button and reset button
        button_frame = tk.Frame(parent, bg=COLORS['ebony'])
        button_frame.pack(pady=10)
        
        # Main quest button
        btn_config = {
            QuestStatus.COMPLETED: ("Replay Quest", COLORS['success_green']),
            QuestStatus.IN_PROGRESS: ("Continue Journey", COLORS['gold']),
            QuestStatus.AVAILABLE: ("Begin Quest", COLORS['periwinkle'])
        }
        btn_text, btn_color = btn_config[status_info.status]
        
        tk.Button(button_frame, text=btn_text, command=lambda c=character: self.start_quest(c),
                 bg=btn_color, fg=COLORS['ebony'], font=('Georgia', 8, 'bold'),
                 relief='raised', borderwidth=2, cursor='hand2', width=15).pack(side=tk.LEFT, padx=2)
        
        # Small reset button for individual character
        tk.Button(button_frame, text="↺", 
                 command=lambda c=character: self.confirm_reset_character(c),
                 bg=COLORS['error_red'], fg=COLORS['gold'],
                 font=('Georgia', 8, 'bold'), width=2,
                 relief='raised', borderwidth=2, cursor='hand2').pack(side=tk.LEFT, padx=2)
    
    def start_quest(self, character: str) -> None:
        """Start or continue a character's quest"""
        quest = self.quests[character]
        progress = self.quest_progress[character]
        
        # Create quest window
        quest_window = tk.Toplevel(self.parent.root)
        quest_window.title(f"{character} - {quest.quest_name}")
        quest_window.configure(bg=COLORS['ebony'])
        quest_window.transient(self.parent.root)
        quest_window.grab_set()
        
        # ALWAYS CENTER the window (ignore window_side setting)
        self.window_manager.center_window(quest_window, 1000, 950)
        
        self.active_quest_window = quest_window
        
        # Add reset button to quest window
        self._add_quest_window_reset(quest_window, character)
        
        # Main container
        main_container = tk.Frame(quest_window, bg=COLORS['ebony'])
        main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Header
        self._create_quest_header(main_container, character, quest)
        
        # Progress bar
        if progress < quest.stage_count:
            self.ui_builder.create_progress_bar(main_container, progress + 1, quest.stage_count)
        
        # Scrollable content
        scrollable, _ = self.window_manager.create_scrollable_frame(main_container, COLORS['ebony'])
        
        # Display current stage
        if progress >= quest.stage_count:
            self._display_quest_finale(scrollable, quest)
        else:
            self._display_quest_stage(scrollable, quest, progress)
    
    def _add_quest_window_reset(self, window: tk.Toplevel, character: str) -> None:
        """Add reset button to quest window"""
        reset_frame = tk.Frame(window, bg=COLORS['ebony'])
        reset_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(reset_frame, text="↺ Reset This Quest",
                 command=lambda: self.confirm_reset_character(character),
                 bg=COLORS['error_red'], fg=COLORS['gold'],
                 font=('Georgia', 9, 'bold'),
                 relief='raised', borderwidth=2,
                 padx=10, pady=2, cursor='hand2').pack(side=tk.RIGHT)
    
    def _create_quest_header(self, parent: tk.Widget, character: str, quest) -> None:
        """Create improved quest window header"""
        char_color = self.parent.characters[character]['color']
        
        # Main header frame with decorative borders
        header = tk.Frame(parent, bg=COLORS['ebony'])
        header.pack(fill=tk.X, pady=(0, 15))
        
        # Top gold border
        tk.Frame(header, bg=COLORS['gold'], height=3).pack(fill=tk.X)
        
        # Character info frame
        info_frame = tk.Frame(header, bg=char_color, height=90)
        info_frame.pack(fill=tk.X)
        info_frame.pack_propagate(False)
        
        # Centered content
        content_frame = tk.Frame(info_frame, bg=char_color)
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Character name and role
        tk.Label(content_frame, text=f"{self.parent.characters[character]['image']}  {character}",
                font=('Georgia', 18, 'bold'), fg=COLORS['gold'],
                bg=char_color).pack(pady=(10, 2))
        
        tk.Label(content_frame, text=f"{quest.role} • {quest.operation} {quest.symbol}",
                font=('Georgia', 13), fg=COLORS['cream'],
                bg=char_color).pack(pady=(0, 10))
        
        # Bottom gold border
        tk.Frame(header, bg=COLORS['gold'], height=3).pack(fill=tk.X)
    
    def _display_quest_stage(self, parent: tk.Widget, quest, stage_num: int) -> None:
        """Display a quest stage with fully improved, centered, readable layout"""
        stage_data = quest.get_stage_data(stage_num)
        
        # Centered container
        center_frame = tk.Frame(parent, bg=COLORS['ebony'])
        center_frame.pack(fill=tk.BOTH, expand=True)
        
        # === SCENE INDICATOR ===
        if 'scene' in stage_data:
            scene_frame = tk.Frame(center_frame, bg=COLORS['shadow'])
            scene_frame.pack(fill=tk.X, pady=(0, 15))
            
            scene_inner = tk.Frame(scene_frame, bg=COLORS['shadow'])
            scene_inner.pack(pady=8)
            
            tk.Label(scene_inner, text=f"📍 {stage_data['scene'].replace('_', ' ').title()}",
                    font=('Georgia', 10, 'italic'),
                    fg=COLORS['periwinkle'], bg=COLORS['shadow']).pack()
        
        # === STAGE TITLE ===
        title_frame = tk.Frame(center_frame, bg=COLORS['gold'], bd=4, relief='ridge')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_inner = tk.Frame(title_frame, bg=COLORS['gold'])
        title_inner.pack(pady=12, padx=20)
        
        tk.Label(title_inner, text=f"Stage {stage_num + 1}: {stage_data['title']}",
                font=('Georgia', 20, 'bold'),
                fg=COLORS['deep_red'], bg=COLORS['gold']).pack()
        
        # === DIALOGUE SCENE (Main reading area) ===
        dialogue_outer = tk.Frame(center_frame, bg=COLORS['gold'], bd=4, relief='ridge')
        dialogue_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        dialogue_header = tk.Frame(dialogue_outer, bg=COLORS['wine'])
        dialogue_header.pack(fill=tk.X)
        
        tk.Label(dialogue_header, text="📜 SCENE 📜",
                font=('Georgia', 12, 'bold'),
                fg=COLORS['cream'], bg=COLORS['wine']).pack(pady=8)
        
        # Scrollable dialogue container
        dialogue_container = tk.Frame(dialogue_outer, bg=COLORS['cream'])
        dialogue_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create scrollable text area
        text_canvas = tk.Canvas(dialogue_container, bg=COLORS['cream'], 
                                highlightthickness=0, insertwidth=0)
        v_scroll = ttk.Scrollbar(dialogue_container, orient=tk.VERTICAL, command=text_canvas.yview)
        h_scroll = ttk.Scrollbar(dialogue_container, orient=tk.HORIZONTAL, command=text_canvas.xview)
        
        text_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        dialogue_inner = tk.Frame(text_canvas, bg=COLORS['cream'])
        
        def on_configure(event):
            text_canvas.configure(scrollregion=text_canvas.bbox("all"))
            text_canvas.yview_moveto(0)
        
        dialogue_inner.bind("<Configure>", on_configure)
        
        text_canvas_window = text_canvas.create_window((0, 0), window=dialogue_inner, anchor="nw")
        
        def on_canvas_configure(event):
            text_canvas.itemconfig(text_canvas_window, width=event.width)
        
        text_canvas.bind("<Configure>", on_canvas_configure)
        
        # Dialogue text content
        dialogue_label = tk.Label(dialogue_inner, text=stage_data['dialogue'],
                                bg=COLORS['cream'], fg=COLORS['deep_red'],
                                font=('Georgia', 13), wraplength=850,
                                justify=tk.LEFT, anchor='nw', padx=30, pady=25)
        dialogue_label.pack(fill=tk.BOTH, expand=True)
        
        # Mousewheel scrolling for dialogue
        def on_dialogue_scroll(event):
            text_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        dialogue_container.bind("<MouseWheel>", on_dialogue_scroll)
        text_canvas.bind("<MouseWheel>", on_dialogue_scroll)
        
        # Layout
        text_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # === CHALLENGE BOX ===
        challenge_outer = tk.Frame(center_frame, bg=COLORS['gold'], bd=4, relief='ridge')
        challenge_outer.pack(fill=tk.X, pady=(0, 20))
        
        challenge_header = tk.Frame(challenge_outer, bg=COLORS['crimson'])
        challenge_header.pack(fill=tk.X)
        
        tk.Label(challenge_header, text="⚔ YOUR CHALLENGE ⚔",
                font=('Georgia', 14, 'bold'),
                fg=COLORS['gold'], bg=COLORS['crimson']).pack(pady=10)
        
        challenge_body = tk.Frame(challenge_outer, bg=COLORS['shadow'])
        challenge_body.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(challenge_body, text=stage_data['challenge'],
                font=('Georgia', 13),
                fg=COLORS['cream'], bg=COLORS['shadow'],
                wraplength=850, justify=tk.CENTER, pady=20).pack(pady=15)
        
        # === LESSON BOX ===
        lesson_frame = tk.Frame(center_frame, bg=COLORS['shadow'], bd=3, relief='ridge')
        lesson_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(lesson_frame, text=f"💡 Key Lesson: {stage_data.get('lesson', '')}",
                font=('Georgia', 12, 'italic'),
                fg=COLORS['terracotta'], bg=COLORS['shadow'],
                wraplength=850, justify=tk.CENTER, pady=15).pack(pady=12)
        
        # === SEPARATOR ===
        tk.Frame(center_frame, bg=COLORS['gold'], height=4).pack(fill=tk.X, pady=10)
        
        # Puzzle area - CENTERED
        puzzle_outer = tk.Frame(center_frame, bg=COLORS['gold'], bd=4, relief='ridge')
        puzzle_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        puzzle_header = tk.Frame(puzzle_outer, bg=COLORS['wine'])
        puzzle_header.pack(fill=tk.X)
        
        tk.Label(puzzle_header, text="🧩 TRUTH TABLE PUZZLE 🧩",
                font=('Georgia', 14, 'bold'),
                fg=COLORS['cream'], bg=COLORS['wine']).pack(pady=10)
        
        puzzle_frame = tk.Frame(puzzle_outer, bg=COLORS['cream'])
        puzzle_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create puzzle
        if stage_data['puzzle_type'] == 'truth_table':
            # Verify puzzle_data exists
            if 'puzzle_data' in stage_data and stage_data['puzzle_data']:
                self.puzzle_manager.create_truth_table_puzzle(
                    puzzle_frame, stage_data['puzzle_data'], stage_data['lesson'],
                    lambda: self._complete_stage(quest, stage_num)
                )
            else:
                # Fallback if puzzle_data is missing
                error_label = tk.Label(puzzle_frame, 
                                      text="Error: Puzzle data missing. Please check quest configuration.",
                                      fg=COLORS['error_red'], bg=COLORS['cream'],
                                      font=('Georgia', 12))
                error_label.pack(pady=30)
        else:
            self._create_special_puzzle(puzzle_frame, stage_data, quest, stage_num)
    
    def _create_special_puzzle(self, parent: tk.Widget, stage_data: Dict, quest, stage_num: int) -> None:
        """Create special puzzle types with interactive user input"""
        self.puzzle_manager.puzzle_lesson = stage_data['lesson']
        self.puzzle_manager.complete_callback = lambda: self._complete_stage(quest, stage_num)
        
        # Create a frame for the puzzle
        puzzle_content = tk.Frame(parent, bg=COLORS['ebony'])
        puzzle_content.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Display puzzle description/instructions
        if 'challenge' in stage_data:
            desc_label = tk.Label(puzzle_content, text=stage_data['challenge'],
                                 font=('Georgia', 11), fg=COLORS['periwinkle'], 
                                 bg=COLORS['ebony'], wraplength=700, justify=tk.CENTER)
            desc_label.pack(pady=10)
        
        # Format and display puzzle data
        puzzle_text = self._format_puzzle_data(stage_data)
        
        # Create a text widget to display the puzzle
        text_frame = tk.Frame(puzzle_content, bg=COLORS['shadow'], bd=2, relief='ridge')
        text_frame.pack(fill=tk.X, pady=10, padx=20)
        
        text_widget = tk.Text(text_frame, height=8, bg=COLORS['shadow'], fg=COLORS['cream'],
                              font=('Courier', 10), wrap=tk.WORD, padx=15, pady=15)
        text_widget.pack(fill=tk.X)
        text_widget.insert(tk.END, puzzle_text)
        text_widget.config(state=tk.DISABLED)
        
        # Create input frame for user answers
        input_frame = tk.Frame(puzzle_content, bg=COLORS['ebony'])
        input_frame.pack(pady=15)
        
        # Store answer variable
        answer_var = tk.StringVar()
        
        # Create appropriate input based on puzzle type
        puzzle_type = stage_data.get('puzzle_id', '')
        
        tk.Label(input_frame, text="Your answer:", 
                font=('Georgia', 10, 'bold'), fg=COLORS['gold'], 
                bg=COLORS['ebony']).pack()
        
        # Create entry field
        answer_entry = tk.Entry(input_frame, textvariable=answer_var,
                               width=40, font=('Georgia', 11),
                               bg=COLORS['cream'], fg=COLORS['deep_red'],
                               justify='center')
        answer_entry.pack(pady=8)
        
        # Function to check the answer
        def check_special_answer():
            answer = answer_var.get().strip().upper()
            
            # For now, we'll accept any non-empty answer
            # You can customize this based on expected answers
            if answer:
                self.puzzle_manager.lesson_label.config(text="✓ " + stage_data['lesson'])
                self.puzzle_manager.payoff_label.config(text=stage_data.get('emotional_payoff', ''))
                if self.puzzle_manager.complete_callback:
                    self.puzzle_manager.complete_callback()
            else:
                self.puzzle_manager.lesson_label.config(text="✗ Please provide an answer")
        
        # Submit button
        submit_btn = tk.Button(input_frame, text="✓ Submit Answer",
                              command=check_special_answer,
                              bg=COLORS['deep_red'], fg=COLORS['gold'],
                              font=('Georgia', 11, 'bold'),
                              relief='raised', borderwidth=2,
                              padx=25, pady=8, cursor='hand2')
        submit_btn.pack(pady=10)
        
        # Labels for feedback
        self.puzzle_manager.lesson_label = tk.Label(puzzle_content, text="", font=('Georgia', 10, 'italic'),
                                                    fg=COLORS['periwinkle'], bg=COLORS['ebony'],
                                                    wraplength=700, justify=tk.CENTER)
        self.puzzle_manager.lesson_label.pack(pady=5)
        
        self.puzzle_manager.payoff_label = tk.Label(puzzle_content, text="", font=('Georgia', 10, 'italic'),
                                                    fg=COLORS['gold'], bg=COLORS['ebony'],
                                                    wraplength=700, justify=tk.CENTER)
        self.puzzle_manager.payoff_label.pack(pady=10)
    
    def _format_puzzle_data(self, stage_data: Dict) -> str:
        """Format puzzle data for display"""
        puzzle_type = stage_data.get('puzzle_id', '')
        puzzle_data = stage_data.get('puzzle_data', {})
        
        if puzzle_type == 'dual_implication':
            return f"""
{puzzle_data.get('title', 'Dual Implication')}

Let A = {puzzle_data.get('A', 'A')}
Let B = {puzzle_data.get('B', 'B')}

Statement 1: {puzzle_data.get('statement1', 'A → C')}
Statement 2: {puzzle_data.get('statement2', 'B → D')}

Given that A and B cannot both be true,
explain why both implications are valid despite the impossible choice.
"""
        elif 'comparison' in puzzle_data:
            if isinstance(puzzle_data, dict) and 'comparison' in puzzle_data:
                return puzzle_data['comparison']
            return str(puzzle_data)
        elif 'analysis' in puzzle_data:
            if isinstance(puzzle_data, dict) and 'analysis' in puzzle_data:
                return puzzle_data['analysis']
            return str(puzzle_data)
        elif 'reflection' in puzzle_data:
            if isinstance(puzzle_data, dict) and 'reflection' in puzzle_data:
                return puzzle_data['reflection']
            return str(puzzle_data)
        elif 'equation' in puzzle_data:
            if isinstance(puzzle_data, dict) and 'equation' in puzzle_data:
                return puzzle_data['equation']
            return str(puzzle_data)
        elif 'matrix' in puzzle_data:
            if isinstance(puzzle_data, dict) and 'matrix' in puzzle_data:
                return puzzle_data['matrix']
            return str(puzzle_data)
        else:
            # If puzzle_data is a string or has a different structure
            if isinstance(puzzle_data, str):
                return puzzle_data
            elif isinstance(puzzle_data, dict):
                # Try to find any meaningful content
                for key in ['title', 'description', 'question']:
                    if key in puzzle_data:
                        return puzzle_data[key]
            return "Contemplate the meaning of this logical truth and provide your answer below."
    
    def _show_special_solution(self, parent: tk.Widget, stage_data: Dict, quest, stage_num: int) -> None:
        """Show solution for special puzzles (kept for backward compatibility)"""
        self.puzzle_manager.lesson_label.config(text="✓ " + stage_data['lesson'])
        self.puzzle_manager.payoff_label.config(text=stage_data.get('emotional_payoff', ''))
        if self.puzzle_manager.complete_callback:
            self.puzzle_manager.complete_callback()
    
    def _display_quest_finale(self, parent: tk.Widget, quest) -> None:
        """Display quest finale with improved centered layout"""
        finale = quest.get_finale()
        
        # Centered container
        center_frame = tk.Frame(parent, bg=COLORS['ebony'])
        center_frame.pack(expand=True, fill=tk.BOTH)
        
        # Scene indicator
        if 'scene' in finale:
            self.ui_builder.create_scene_indicator(center_frame, finale['scene'])
        
        # Decorative top border
        tk.Frame(center_frame, bg=COLORS['gold'], height=3).pack(fill=tk.X, pady=(10, 15))
        
        # Title with decorative frame
        title_frame = tk.Frame(center_frame, bg=COLORS['shadow'], bd=3, relief='ridge')
        title_frame.pack(fill=tk.X, padx=40, pady=(0, 15))
        
        title_inner = tk.Frame(title_frame, bg=COLORS['gold'], bd=2, relief='solid')
        title_inner.pack(expand=True, fill=tk.BOTH, padx=3, pady=3)
        
        tk.Label(title_inner, text=finale['title'], font=('Georgia', 18, 'bold'),
                fg=COLORS['deep_red'], bg=COLORS['gold']).pack(pady=8, padx=10)
        
        # Dialogue with larger font
        self.ui_builder.create_dialogue_box(center_frame, finale['dialogue'], height=14)
        
        # Decorative separator
        sep_frame = tk.Frame(center_frame, bg=COLORS['ebony'], height=30)
        sep_frame.pack(fill=tk.X, pady=10)
        tk.Frame(sep_frame, bg=COLORS['gold'], height=2).pack(fill=tk.X, padx=200)
        
        # Reward section
        reward_frame = tk.Frame(center_frame, bg=COLORS['shadow'], bd=3, relief='groove')
        reward_frame.pack(fill=tk.X, padx=40, pady=10)
        
        reward_inner = tk.Frame(reward_frame, bg=COLORS['shadow'], bd=2, relief='solid')
        reward_inner.pack(expand=True, fill=tk.BOTH, padx=3, pady=3)
        
        tk.Label(reward_inner, text="✨ QUEST COMPLETE ✨", font=('Georgia', 16, 'bold'),
                fg=COLORS['gold'], bg=COLORS['shadow']).pack(pady=8)
        
        tk.Label(reward_inner, text=finale['reward'], font=('Georgia', 12),
                fg=COLORS['periwinkle'], bg=COLORS['shadow'],
                wraplength=800, justify=tk.CENTER).pack(pady=5, padx=10)
        
        if 'unlock_song' in finale:
            tk.Label(reward_inner, text=f"🔓 Unlocked: {finale['unlock_song']}",
                    font=('Georgia', 13, 'bold italic'),
                    fg=COLORS['success_green'], bg=COLORS['shadow']).pack(pady=8)
        
        # Decorative bottom border
        tk.Frame(center_frame, bg=COLORS['gold'], height=3).pack(fill=tk.X, pady=(15, 10))
        
        # Finish button with hover effect
        btn_frame = tk.Frame(center_frame, bg=COLORS['ebony'])
        btn_frame.pack(pady=15)
        
        finish_btn = tk.Button(btn_frame, text="Return to Grimoire",
                 command=self.close_quest_window,
                 bg=COLORS['deep_red'], fg=COLORS['gold'],
                 font=('Georgia', 13, 'bold'),
                 padx=40, pady=12, cursor='hand2',
                 relief='raised', bd=3)
        finish_btn.pack()
        
        finish_btn.bind('<Enter>', lambda e: finish_btn.config(bg=COLORS['success_green']))
        finish_btn.bind('<Leave>', lambda e: finish_btn.config(bg=COLORS['deep_red']))
    
    def _complete_stage(self, quest, stage_num: int) -> None:
        """Complete current stage and advance to next"""
        # Update progress
        self.quest_progress[quest.character] = stage_num + 1
        
        # Check if quest is now completed
        if stage_num + 1 >= quest.stage_count:
            # Quest completed
            self.quest_completed[quest.character] = True
            if quest.character not in self.completed_quests:
                self.completed_quests.append(quest.character)
            
            # Unlock corresponding song
            self._unlock_song_for_character(quest.character)
            
            # Show completion message
            messagebox.showinfo("Quest Complete!", 
                              f"Congratulations! You've completed {quest.character}'s quest!\n\n"
                              f"✨ {quest.quest_name} ✨\n\n"
                              f"Reward: {quest.get_finale().get('unlock_song', 'Mastery achieved!')}")
        
        # Save progress immediately
        self.save_progress()
        
        # Force update of the quest object's current_stage
        if hasattr(quest, 'current_stage'):
            quest.current_stage = self.quest_progress[quest.character]
        
        # Close current window
        if self.active_quest_window:
            self.active_quest_window.destroy()
            self.active_quest_window = None
        
        # Force multiple refreshes to ensure UI updates
        self.parent.refresh_character_encounters()
        self.parent.update_songs_display()
        self.parent.root.update_idletasks()
    
    def _unlock_song_for_character(self, character: str) -> None:
        """Unlock song corresponding to completed character quest"""
        song_map = {
            'Sakiko Togawa': 'Masquerade Rhapsody Request',
            'Uika Misumi': 'Angles',
            'Mutsumi Wakaba': "Choir 'S' Choir",
            'Umiri Yahata': "'S/' The Way",
            'Nyamu Yūtenji': 'Blue Eyes'
        }
        
        if character in song_map:
            song_name = song_map[character]
            for song in self.parent.ave_mujica_songs:
                if song['title'] == song_name and song not in self.parent.unlocked_songs:
                    self.parent.unlocked_songs.append(song)
                    break
            
            # Also unlock song in music player
            if hasattr(self.parent, 'music_player'):
                self.parent.music_player.unlock_character_song(character)
    
    def close_quest_window(self) -> None:
        """Close the active quest window"""
        if self.active_quest_window:
            self.active_quest_window.destroy()
            self.active_quest_window = None
        
        self.parent.refresh_character_encounters()
        
        # Check if all quests are completed
        if all(self.quest_completed.values()) and not self.final_shown:
            self.final_shown = True
            self._show_final_quest_notification()
    
    def _show_final_quest_notification(self) -> None:
        """Show notification that final quest is unlocked"""
        # Check if all 16 gates are also completed for secret ending
        all_gates_completed = False
        if hasattr(self.parent, 'quiz_manager'):
            total_questions = self.parent.quiz_manager.total_questions
            answered = self.parent.quiz_manager.questions_answered
            all_gates_completed = answered >= total_questions
        
        # Unlock secret ending if both conditions met
        if all_gates_completed and hasattr(self.parent, 'music_player'):
            self.parent.music_player.unlock_secret_ending()
        
        if all_gates_completed:
            messagebox.showinfo("🔮 TRUE SECRET ENDING UNLOCKED 🔮",
                              "You have completed ALL 16 Gates of Truth AND all 5 Character Quests!\n\n"
                              "The TRUE ending beyond the masquerade awaits...\n\n"
                              "Would you like to experience it now?")
        else:
            result = messagebox.askyesno("🔮 The Final Masquerade 🔮",
                                        "You have completed all character quests!\n\n"
                                        "The final truth of Ave Mujica awaits...\n\n"
                                        f"(Complete all 16 Gates for the TRUE secret ending: {len(self.parent.ave_mujica_songs) if hasattr(self.parent, 'ave_mujica_songs') else 16}/{len(self.parent.unlocked_songs) if hasattr(self.parent, 'unlocked_songs') else 0})\n\n"
                                        "Would you like to experience it now?")
            if result:
                self.show_final_quest()
    
    def show_final_quest(self) -> None:
        """Show the final integration quest"""
        if not self.final_quest:
            return
            
        finale = self.final_quest.get_finale()
        
        final_window = tk.Toplevel(self.parent.root)
        final_window.title("The Masquerade's Truth")
        final_window.configure(bg=COLORS['ebony'])
        final_window.transient(self.parent.root)
        final_window.grab_set()
        
        # Position final quest window based on preferred side
        if self.window_side == 'center':
            self.window_manager.center_window(final_window, 1000, 800)
        else:
            self.window_manager.position_window_on_side(
                final_window, self.parent.root, 1000, 700, self.window_side
            )
        
        # Scrollable content
        scrollable, _ = self.window_manager.create_scrollable_frame(final_window, COLORS['ebony'])
        
        # Header
        self.window_manager.create_header(scrollable, finale['title'], "The Final Revelation")
        
        # Scene
        if 'scene' in finale:
            self.ui_builder.create_scene_indicator(scrollable, finale['scene'])
        
        # Dialogue
        self.ui_builder.create_dialogue_box(scrollable, finale['dialogue'], height=15)
        
        # Reward
        reward_frame = tk.Frame(scrollable, bg=COLORS['shadow'], bd=2, relief='ridge')
        reward_frame.pack(fill=tk.X, pady=20)
        
        reward_text = tk.Text(reward_frame, height=20, bg=COLORS['shadow'],
                              fg=COLORS['periwinkle'], font=('Courier', 10),
                              wrap=tk.WORD, padx=20, pady=20)
        reward_text.pack(fill=tk.X)
        reward_text.insert(tk.END, finale['reward'])
        reward_text.config(state=tk.DISABLED)
        
        # Close button
        tk.Button(scrollable, text="Return to Grimoire",
                 command=final_window.destroy,
                 bg=COLORS['deep_red'], fg=COLORS['gold'],
                 font=('Georgia', 12, 'bold'),
                 padx=30, pady=10, cursor='hand2').pack(pady=20)
    
    def create_quest_selector(self, parent: tk.Widget) -> None:
        """Create quest selection interface"""
        selector_frame = tk.Frame(parent, bg=COLORS['ebony'])
        selector_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Header with reset button
        header_frame = tk.Frame(selector_frame, bg=COLORS['ebony'])
        header_frame.pack(fill=tk.X)
        
        # Title on left
        title_frame = tk.Frame(header_frame, bg=COLORS['ebony'])
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(title_frame, text="🔮 CHARACTER QUESTS 🔮",
                font=('Georgia', 24, 'bold'), fg=COLORS['gold'], 
                bg=COLORS['ebony']).pack(anchor='center')
        
        tk.Label(title_frame, text="Embark on personal journeys with each band member",
                font=('Georgia', 12, 'italic'), fg=COLORS['periwinkle'], 
                bg=COLORS['ebony']).pack(anchor='center', pady=5)
        
        # Reset button on right
        reset_btn = tk.Button(header_frame, text="⟲ Reset All Progress",
                             command=self.confirm_reset_all,
                             bg=COLORS['error_red'], fg=COLORS['gold'],
                             font=('Georgia', 10, 'bold'),
                             relief='raised', borderwidth=2,
                             padx=15, pady=5, cursor='hand2')
        reset_btn.pack(side=tk.RIGHT, padx=10)
        
        # Individual reset buttons for each character
        reset_frame = tk.Frame(selector_frame, bg=COLORS['ebony'])
        reset_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(reset_frame, text="Reset Individual Quests:",
                font=('Georgia', 10, 'bold'), fg=COLORS['cream'],
                bg=COLORS['ebony']).pack(side=tk.LEFT, padx=5)
        
        for character in self.quests.keys():
            char_btn = tk.Button(reset_frame, text=character.split()[0],
                                command=lambda c=character: self.confirm_reset_character(c),
                                bg=COLORS['deep_red'], fg=COLORS['gold'],
                                font=('Georgia', 8, 'bold'),
                                relief='raised', borderwidth=1,
                                padx=8, pady=2, cursor='hand2')
            char_btn.pack(side=tk.LEFT, padx=2)
        
        # Separator
        tk.Frame(selector_frame, bg=COLORS['gold'], height=2).pack(fill=tk.X, pady=10)
        
        # Cards container
        cards_container = tk.Frame(selector_frame, bg=COLORS['ebony'])
        cards_container.pack(expand=True, pady=20)
        
        cards_frame = tk.Frame(cards_container, bg=COLORS['ebony'])
        cards_frame.pack()
        
        # Create cards grid
        row, col = 0, 0
        for character, quest in self.quests.items():
            status = self.get_quest_status(character)
            
            # Determine border color
            border_color = {
                QuestStatus.COMPLETED: COLORS['success_green'],
                QuestStatus.IN_PROGRESS: COLORS['gold'],
                QuestStatus.AVAILABLE: self.parent.characters[character]['color']
            }[status.status]
            
            # Create card
            card = tk.Frame(cards_frame, bg=border_color, bd=3, relief='raised')
            card.grid(row=row, column=col, padx=15, pady=15, ipadx=5, ipady=5)
            
            self._create_quest_selector_card(card, character, quest, status)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Check for final quest
        if all(self.quest_completed.values()):
            self._show_final_quest_button(selector_frame)
    
    def _create_quest_selector_card(self, parent: tk.Widget, character: str,
                                    quest, status: QuestStatusInfo) -> None:
        """Create a quest selector card"""
        # Status bar
        status_frame = tk.Frame(parent, bg=status.color)
        status_frame.pack(fill=tk.X)
        
        tk.Label(status_frame, text=f"{status.icon} {status.display_text}",
                font=('Georgia', 8, 'bold'), fg=COLORS['ebony'],
                bg=status.color).pack()
        
        # Card content
        inner = tk.Frame(parent, bg=COLORS['ebony'], bd=2, relief='sunken')
        inner.pack(padx=5, pady=5)
        
        # Character image
        tk.Label(inner, text=self.parent.characters[character]['image'],
                font=('Georgia', 32), bg=COLORS['ebony'],
                fg=self.parent.characters[character]['color']).pack(pady=10)
        
        # Name
        tk.Label(inner, text=character, font=('Georgia', 12, 'bold'),
                fg=COLORS['gold'], bg=COLORS['ebony']).pack()
        
        # Role
        tk.Label(inner, text=self.parent.characters[character]['role'],
                font=('Georgia', 10, 'italic'), fg=COLORS['periwinkle'],
                bg=COLORS['ebony']).pack()
        
        # Operation
        tk.Label(inner, text=f"{quest.symbol} {quest.operation}",
                font=('Georgia', 10, 'bold'), fg=COLORS['terracotta'],
                bg=COLORS['ebony']).pack(pady=5)
        
        # Quest name
        tk.Label(inner, text=quest.quest_name, font=('Georgia', 9),
                fg=COLORS['cream'], bg=COLORS['ebony'], wraplength=180).pack(pady=5)
        
        # Progress
        tk.Label(inner, text=status.progress_text, font=('Georgia', 8),
                fg=status.color, bg=COLORS['ebony']).pack()
        
        # Button frame
        button_frame = tk.Frame(inner, bg=COLORS['ebony'])
        button_frame.pack(pady=5)
        
        # Main action button
        btn_text = {
            QuestStatus.COMPLETED: "Replay Quest",
            QuestStatus.IN_PROGRESS: "Continue",
            QuestStatus.AVAILABLE: "Start Quest"
        }[status.status]
        
        tk.Button(button_frame, text=btn_text, 
                 command=lambda c=character: self.start_quest(c),
                 bg=COLORS['deep_red'], fg=COLORS['gold'],
                 font=('Georgia', 9, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=2)
        
        # Reset button for this character
        tk.Button(button_frame, text="↺",
                 command=lambda c=character: self.confirm_reset_character(c),
                 bg=COLORS['error_red'], fg=COLORS['gold'],
                 font=('Georgia', 9, 'bold'), width=2,
                 cursor='hand2').pack(side=tk.LEFT, padx=2)
    
    def _show_final_quest_button(self, parent: tk.Widget) -> None:
        """Show final quest button after all quests completed"""
        final_frame = tk.Frame(parent, bg=COLORS['gold'], bd=3, relief='raised')
        final_frame.pack(fill=tk.X, pady=30)
        
        tk.Label(final_frame, text="🔮 THE FINAL MASQUERADE 🔮",
                font=('Georgia', 18, 'bold'), fg=COLORS['deep_red'],
                bg=COLORS['gold']).pack(pady=10)
        
        tk.Label(final_frame, text="All character quests complete. The ultimate truth awaits...",
                font=('Georgia', 11), fg=COLORS['ebony'], bg=COLORS['gold']).pack()
        
        button_frame = tk.Frame(final_frame, bg=COLORS['gold'])
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Experience the Final Truth",
                 command=self.show_final_quest, bg=COLORS['deep_red'],
                 fg=COLORS['gold'], font=('Georgia', 12, 'bold'),
                 padx=30, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="↺ Reset All",
                 command=self.confirm_reset_all,
                 bg=COLORS['error_red'], fg=COLORS['gold'],
                 font=('Georgia', 10, 'bold'),
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
    
    def confirm_reset_character(self, character: str) -> None:
        """Confirm resetting a single character's quest"""
        result = messagebox.askyesno(
            "Reset Character Quest",
            f"Are you sure you want to reset {character}'s quest progress?\n\n"
            "This will erase all progress and set the quest back to available.\n"
            "Any unlocked songs from this quest will be locked again."
        )
        
        if result:
            self.reset_character_quest(character)
    
    def confirm_reset_all(self) -> None:
        """Confirm resetting all quest progress"""
        result = messagebox.askyesno(
            "Reset All Progress",
            "⚠️ WARNING: This will reset ALL character quest progress!\n\n"
            "• All quest progress will be lost\n"
            "• All unlocked songs from quests will be removed\n"
            "• All characters will be set to 'Available'\n"
            "• The final quest will be locked again\n\n"
            "Are you absolutely sure you want to continue?"
        )
        
        if result:
            # Double-check with a second confirmation
            result2 = messagebox.askyesno(
                "Final Confirmation",
                "This action cannot be undone!\n\n"
                "Are you REALLY sure you want to reset everything?"
            )
            
            if result2:
                self.reset_all_progress()
    
    def reset_character_quest(self, character: str) -> None:
        """Reset a single character's quest progress"""
        if character in self.quests:
            old_completed = self.quest_completed[character]
            
            # Reset progress tracking
            self.quest_progress[character] = 0
            self.quest_completed[character] = False
            
            # Remove from completed quests list
            if character in self.completed_quests:
                self.completed_quests.remove(character)
            
            # Remove unlocked song if this character's quest completion unlocked it
            if old_completed:
                song_map = {
                    'Sakiko Togawa': 'Masquerade Rhapsody Request',
                    'Uika Misumi': 'Angles',
                    'Mutsumi Wakaba': "Choir 'S' Choir",
                    'Umiri Yahata': "'S/' The Way",
                    'Nyamu Yūtenji': 'Blue Eyes'
                }
                
                if character in song_map:
                    song_name = song_map[character]
                    # Remove from unlocked songs
                    self.parent.unlocked_songs = [s for s in self.parent.unlocked_songs 
                                                 if s['title'] != song_name]
                    
                    # Also reset in music player
                    if hasattr(self.parent, 'music_player'):
                        self.parent.music_player.reset_character_songs()
            
            # CRITICAL: Reset the quest object's internal state
            quest_obj = self.quests[character]
            
            # Reset current_stage if it exists
            if hasattr(quest_obj, 'current_stage'):
                quest_obj.current_stage = 0
                print(f"Reset {character}.current_stage to 0")
            
            # Reset completed flag if it exists
            if hasattr(quest_obj, 'completed'):
                quest_obj.completed = False
                print(f"Reset {character}.completed to False")
            
            # Reset stage count to beginning if the quest has a reset method
            if hasattr(quest_obj, 'reset'):
                quest_obj.reset()
            
            # Some quest classes might have different attribute names
            if hasattr(quest_obj, 'stage'):
                quest_obj.stage = 0
            if hasattr(quest_obj, 'current'):
                quest_obj.current = 0
            if hasattr(quest_obj, 'progress'):
                quest_obj.progress = 0
            
            # Save progress
            self.save_progress()
            
            # Also update the progress file immediately to reflect 0
            if os.path.exists(self.progress_file):
                try:
                    with open(self.progress_file, 'r') as f:
                        progress_data = json.load(f)
                    
                    progress_data['quest_progress'][character] = 0
                    progress_data['quest_completed'][character] = False
                    if character in progress_data['completed_quests']:
                        progress_data['completed_quests'].remove(character)
                    
                    with open(self.progress_file, 'w') as f:
                        json.dump(progress_data, f, indent=2)
                except:
                    pass
            
            # Force multiple refreshes to ensure UI updates
            if hasattr(self.parent, 'refresh_character_encounters'):
                self.parent.refresh_character_encounters()
            if hasattr(self.parent, 'update_songs_display'):
                self.parent.update_songs_display()
            
            # Force the main window to update
            self.parent.root.update_idletasks()
            self.parent.root.update()  # Additional force update
            
            # If this was the active quest window, close it
            if self.active_quest_window:
                self.active_quest_window.destroy()
                self.active_quest_window = None
            
            messagebox.showinfo("Quest Reset", f"{character}'s quest has been reset successfully!")
            
            # Debug print to verify reset
            print(f"RESET COMPLETE: {character} - progress: {self.quest_progress[character]}, completed: {self.quest_completed[character]}")
            if hasattr(quest_obj, 'current_stage'):
                print(f"  Quest object current_stage: {quest_obj.current_stage}")
    
    def reset_all_progress(self) -> None:
        """Reset all quest progress"""
        # Delete the progress file to start completely fresh
        if os.path.exists(self.progress_file):
            try:
                os.remove(self.progress_file)
                print("Progress file deleted")
            except Exception as e:
                print(f"Could not delete progress file: {e}")
        
        # Reset all quest progress
        for character in self.quests.keys():
            self.quest_progress[character] = 0
            self.quest_completed[character] = False
            
            # CRITICAL: Reset each quest object's internal state
            quest_obj = self.quests[character]
            
            # Reset current_stage if it exists
            if hasattr(quest_obj, 'current_stage'):
                quest_obj.current_stage = 0
                print(f"Reset {character}.current_stage to 0")
            
            # Reset completed flag if it exists
            if hasattr(quest_obj, 'completed'):
                quest_obj.completed = False
                print(f"Reset {character}.completed to False")
            
            # Reset stage count to beginning if the quest has a reset method
            if hasattr(quest_obj, 'reset'):
                quest_obj.reset()
            
            # Some quest classes might have different attribute names
            if hasattr(quest_obj, 'stage'):
                quest_obj.stage = 0
            if hasattr(quest_obj, 'current'):
                quest_obj.current = 0
            if hasattr(quest_obj, 'progress'):
                quest_obj.progress = 0
            
            # Reset any additional state
            if hasattr(quest_obj, 'reset_state'):
                quest_obj.reset_state()
        
        self.completed_quests = []
        self.final_shown = False
        
        # Clear all unlocked songs from quests
        self.parent.unlocked_songs = []
        
        # Reset music player
        if hasattr(self.parent, 'music_player'):
            self.parent.music_player.reset_character_songs()
            self.parent.music_player.reset_gate_songs()
            self.parent.music_player.reset_secret_ending()
        
        # Save progress
        self.save_progress()
        
        # Force multiple refreshes to ensure UI updates
        if hasattr(self.parent, 'refresh_character_encounters'):
            self.parent.refresh_character_encounters()
        if hasattr(self.parent, 'update_songs_display'):
            self.parent.update_songs_display()
        
        # Force the main window to update multiple times
        self.parent.root.update_idletasks()
        self.parent.root.update()  # Additional force update
        
        # If there's an active quest window, close it
        if self.active_quest_window:
            self.active_quest_window.destroy()
            self.active_quest_window = None
        
        messagebox.showinfo("Progress Reset", 
                           "All quest progress has been reset successfully!\n\n"
                           "You can now start your journey anew!")
        
        # Debug print to verify reset
        print(f"RESET ALL COMPLETE - Progress: {self.quest_progress}, Completed: {self.quest_completed}")
        for character in self.quests.keys():
            if hasattr(self.quests[character], 'current_stage'):
                print(f"  {character} current_stage: {self.quests[character].current_stage}")
    
    def save_progress(self) -> None:
        """Save quest progress to file"""
        try:
            progress_data = {
                'quest_progress': self.quest_progress,
                'quest_completed': {k: v for k, v in self.quest_completed.items()},
                'completed_quests': self.completed_quests,
                'final_shown': self.final_shown,
                'window_side': self.window_side
            }
            
            with open(self.progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
            print(f"Progress saved: {progress_data}")  # Debug print
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def load_progress(self) -> None:
        """Load quest progress from file - FIXED VERSION"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    progress_data = json.load(f)
                
                # Validate the loaded data
                if not isinstance(progress_data, dict):
                    print("Invalid progress data format, starting fresh")
                    self._reset_to_initial_state()
                    return
                
                # Initialize with defaults first
                for character in self.quests.keys():
                    self.quest_progress[character] = 0
                    self.quest_completed[character] = False
                
                # Restore progress from file if valid
                saved_progress = progress_data.get('quest_progress', {})
                if isinstance(saved_progress, dict):
                    for character in self.quest_progress.keys():
                        if character in saved_progress:
                            # Only load if it's a valid number
                            try:
                                val = int(saved_progress[character])
                                if 0 <= val <= self.quests[character].stage_count:
                                    self.quest_progress[character] = val
                            except (ValueError, TypeError):
                                pass
                
                # Restore completed status
                saved_completed = progress_data.get('quest_completed', {})
                if isinstance(saved_completed, dict):
                    for character in self.quest_completed.keys():
                        if character in saved_completed and saved_completed[character]:
                            # Only mark as completed if progress indicates it's actually complete
                            if self.quest_progress[character] >= self.quests[character].stage_count:
                                self.quest_completed[character] = True
                            else:
                                self.quest_completed[character] = False
                
                self.completed_quests = progress_data.get('completed_quests', [])
                # Filter completed_quests to only include actually completed quests
                self.completed_quests = [c for c in self.completed_quests 
                                        if c in self.quest_completed and self.quest_completed[c]]
                
                self.final_shown = progress_data.get('final_shown', False)
                self.window_side = progress_data.get('window_side', 'right')
                
                # Update quest objects' internal state
                for character in self.quests.keys():
                    if hasattr(self.quests[character], 'current_stage'):
                        self.quests[character].current_stage = self.quest_progress.get(character, 0)
                    if hasattr(self.quests[character], 'completed'):
                        self.quests[character].completed = self.quest_completed.get(character, False)
                
                print(f"Progress loaded: {progress_data}")
                print(f"Processed state - Progress: {self.quest_progress}, Completed: {self.quest_completed}")
                
            except Exception as e:
                print(f"Error loading progress: {e}")
                self._reset_to_initial_state()
        else:
            # No progress file exists, start fresh
            self._reset_to_initial_state()
            print("No progress file found, starting fresh")
    
    def _reset_to_initial_state(self) -> None:
        """Reset all quest progress to initial state - HELPER METHOD"""
        # Reset all quest progress
        for character in self.quests.keys():
            self.quest_progress[character] = 0
            self.quest_completed[character] = False
            
            # Reset the quest object's internal state
            quest_obj = self.quests[character]
            if hasattr(quest_obj, 'current_stage'):
                quest_obj.current_stage = 0
            if hasattr(quest_obj, 'completed'):
                quest_obj.completed = False
            
            # Reset stage count to beginning if the quest has a reset method
            if hasattr(quest_obj, 'reset'):
                quest_obj.reset()
            
            # Reset any additional state
            if hasattr(quest_obj, 'reset_state'):
                quest_obj.reset_state()
        
        self.completed_quests = []
        self.final_shown = False
        
        # Clear unlocked songs
        if hasattr(self.parent, 'unlocked_songs'):
            self.parent.unlocked_songs = []
        
        # Save the fresh state
        self.save_progress()
        
        # Refresh UI
        if hasattr(self.parent, 'refresh_character_encounters'):
            self.parent.refresh_character_encounters()
        if hasattr(self.parent, 'update_songs_display'):
            self.parent.update_songs_display()
        
        print("Reset to initial state")


# Add this at the end of the file to explicitly export the classes
__all__ = ['CharacterQuestSystem', 'WindowManager', 'UIBuilder', 'QuestStatus', 'QuestStatusInfo', 'PuzzleManager']