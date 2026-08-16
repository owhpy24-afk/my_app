import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

class RoundedButton(Button):
    def __init__(self, bg_color=(0.2, 0.22, 0.25, 1), text_color=(1, 1, 1, 1), font_size='16sp', **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = text_color
        self.bold = True
        self.font_size = font_size
        self.bg_color = bg_color
        
        with self.canvas.before:
            self.color_instruction = Color(*self.bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
            
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class BtnCell(BoxLayout):
    def __init__(self, btn_text, top_markup="", bg_color=(0.2, 0.22, 0.25, 1), text_color=(1, 1, 1, 1), font_size='16sp', **kwargs):
        super().__init__(orientation='vertical', spacing=1, padding=0, **kwargs)
        
        self.top_label = Label(
            text=top_markup, 
            markup=True,
            font_size='11sp',
            bold=True, 
            size_hint=(1, 0.30),
            halign='center',
            valign='bottom'
        )
        self.top_label.bind(size=self.top_label.setter('text_size'))
        self.add_widget(self.top_label)
        
        self.btn = RoundedButton(
            text=btn_text, 
            bg_color=bg_color, 
            text_color=text_color,
            font_size=font_size,
            size_hint=(1, 0.70)
        )
        self.add_widget(self.btn)

class PerfectCasioCalc(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=[6, 6, 6, 6], spacing=3)
        
        self.expr_text = ""
        self.cursor_pos = 0
        self.last_ans = ""
        
        self.shift_active = False
        self.alpha_active = False
        self.hyp_active = False
        self.memory_active = False

        # --- شاشة العرض الحالية بنفس مقاساتها المطلوبة ---
        display_box = BoxLayout(orientation='vertical', size_hint_y=0.32, padding=[12, 6])
        
        with display_box.canvas.before:
            Color(0.70, 0.76, 0.72, 1)
            self.disp_rect = RoundedRectangle(size=display_box.size, pos=display_box.pos, radius=[8])
            
        display_box.bind(pos=self.update_disp_bg, size=self.update_disp_bg)

        self.status_label = Label(
            text="", 
            markup=True,
            font_size='11sp', 
            bold=True,
            size_hint_y=0.20,
            halign='left',
            valign='top'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        display_box.add_widget(self.status_label)

        self.display = Label(
            text='|', 
            font_size='32sp', 
            bold=True,
            color=(0.05, 0.08, 0.25, 1),
            size_hint_y=0.80, 
            halign='left',
            valign='middle'
        )
        self.display.bind(size=self.display.setter('text_size'))
        display_box.add_widget(self.display)
        
        root.add_widget(display_box)
        self.update_status_bar()

        GOLD = "[color=e6b800]"
        PURP = "[color=a680b8]"
        ENDC = "[/color]"
        
        C_SHIFT = (0.85, 0.6, 0.1, 1)
        C_ALPHA = (0.4, 0.35, 0.55, 1)
        C_ORANGE = (0.85, 0.45, 0.15, 1)
        C_DARK = (0.2, 0.22, 0.25, 1)

        # --- لوحة الأزرار العلمية العلوية (تمت إضافة ∧ و ∨ في صف الاتجاهات) ---
        grid_top = GridLayout(cols=6, spacing=2, size_hint_y=0.40)
        
        top_btn_data = [
            ("SHIFT", f"{GOLD}SOLVE{ENDC} {PURP}={ENDC}", C_SHIFT, (0,0,0,1), '12sp'),
            ("ALPHA", f"{GOLD}d/dx{ENDC} {PURP}:{ENDC}", C_ALPHA, (1,1,1,1), '12sp'),
            ("∧", "", C_DARK, (1,1,1,1), '16sp'),  # زرار فوق
            ("∨", "", C_DARK, (1,1,1,1), '16sp'),  # زرار تحت
            ("<", "", C_DARK, (1,1,1,1), '16sp'),  # زرار شمال
            (">", "", C_DARK, (1,1,1,1), '16sp'),  # زرار يمين
            
            ("CALC", f"{GOLD}mod{ENDC} {PURP}+R{ENDC}", C_DARK, (1,1,1,1), '11sp'),
            ("∫dx", f"{GOLD}³√{ENDC}", C_DARK, (1,1,1,1), '12sp'),
            ("^", f"{GOLD}x³{ENDC}", C_DARK, (1,1,1,1), '16sp'),
            ("v", f"{GOLD}ⁿ√{ENDC}", C_DARK, (1,1,1,1), '16sp'),
            ("x⁻¹", f"{GOLD}10ˣ{ENDC}", C_DARK, (1,1,1,1), '12sp'),
            ("Log_a", f"{GOLD}eⁿ{ENDC}", C_DARK, (1,1,1,1), '11sp'),
            
            ("a/b", f"{GOLD}∠{ENDC} {PURP}a{ENDC}", C_DARK, (1,1,1,1), '12sp'),
            ("√", f"{GOLD}FACT{ENDC} {PURP}b{ENDC}", C_DARK, (1,1,1,1), '18sp'),
            ("x²", f"{GOLD}Abs{ENDC} {PURP}c{ENDC}", C_DARK, (1,1,1,1), '13sp'),
            ("xⁿ", f"{GOLD}Sin⁻¹{ENDC} {PURP}d{ENDC}", C_DARK, (1,1,1,1), '12sp'),
            ("Log", f"{GOLD}Cos⁻¹{ENDC} {PURP}e{ENDC}", C_DARK, (1,1,1,1), '12sp'),
            ("Ln", f"{GOLD}Tan⁻¹{ENDC} {PURP}f{ENDC}", C_DARK, (1,1,1,1), '12sp'),
            
            ("(-)", f"{GOLD}STO{ENDC} {PURP}CLRv{ENDC}", C_DARK, (1,1,1,1), '12sp'),
            ("°'\"", f"{GOLD}i{ENDC} {PURP}Cot{ENDC}", C_DARK, (1,1,1,1), '12sp'),
            ("hyp", f"{GOLD}%{ENDC} {PURP}Cot⁻¹{ENDC}", C_DARK, (1,1,1,1), '12sp'),
            ("Sin", f"{GOLD},{ENDC} {PURP}x{ENDC}", C_DARK, (1,1,1,1), '13sp'),
            ("Cos", f"{GOLD}aᵇ/ᶜ{ENDC} {PURP}y{ENDC}", C_DARK, (1,1,1,1), '13sp'),
            ("Tan", f"{GOLD}M-{ENDC} {PURP}m{ENDC}", C_DARK, (1,1,1,1), '13sp'),
            
            ("RCL", f"{GOLD}CONST{ENDC}", C_DARK, (1,1,1,1), '11sp'),
            ("ENG", f"{GOLD}CONV{ENDC}", C_DARK, (1,1,1,1), '11sp'),
            ("(", f"{GOLD}Limit{ENDC}", C_DARK, (1,1,1,1), '16sp'),
            (")", f"{GOLD}∞{ENDC}", C_DARK, (1,1,1,1), '16sp'),
            ("S⇔D", "", C_DARK, (1,1,1,1), '11sp'),
            ("M+", "", C_DARK, (1,1,1,1), '11sp'),
        ]

        for text, markup, bg, fg, fsize in top_btn_data:
            cell = BtnCell(btn_text=text, top_markup=markup, bg_color=bg, text_color=fg, font_size=fsize)
            cell.btn.bind(on_press=self.on_press)
            grid_top.add_widget(cell)

        root.add_widget(grid_top)

        # --- لوحة الأرقام السفلية كما هي بنفس الحجم ---
        grid_bottom = GridLayout(cols=5, spacing=2, size_hint_y=0.28)

        bottom_btn_data = [
            ("7", f"{GOLD}MATRIX{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("8", f"{GOLD}VECTOR{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("9", f"{GOLD}HELP{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("DEL", f"{GOLD}nPr{ENDC} {PURP}GCD{ENDC}", C_ORANGE, (1,1,1,1), '14sp'),
            ("AC", f"{GOLD}nCr{ENDC} {PURP}LCM{ENDC}", C_ORANGE, (1,1,1,1), '14sp'),
            
            ("4", f"{GOLD}STAT{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("5", f"{GOLD}CMPLX{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("6", f"{GOLD}DISTR{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("×", f"{GOLD}Pol{ENDC} {PURP}Ceil{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("÷", f"{GOLD}Rec{ENDC} {PURP}Floor{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            
            ("1", f"{GOLD}COPY{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("2", f"{GOLD}PASTE{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("3", f"{GOLD}Ran#{ENDC} {PURP}RanInt{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("+", f"{GOLD}π{ENDC} {PURP}e{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            ("-", f"{GOLD}PreAns{ENDC}", C_DARK, (1,1,1,1), '20sp'),
            
            ("0", "", C_DARK, (1,1,1,1), '20sp'),
            (".", "", C_DARK, (1,1,1,1), '20sp'),
            ("Exp", "", C_DARK, (1,1,1,1), '14sp'),
            ("Ans", f"{GOLD}History{ENDC}", C_DARK, (1,1,1,1), '14sp'),
            ("=", "", C_DARK, (1,1,1,1), '20sp'),
        ]

        for text, markup, bg, fg, fsize in bottom_btn_data:
            cell = BtnCell(btn_text=text, top_markup=markup, bg_color=bg, text_color=fg, font_size=fsize)
            cell.btn.bind(on_press=self.on_press)
            grid_bottom.add_widget(cell)

        root.add_widget(grid_bottom)
        return root

    def update_disp_bg(self, instance, value):
        self.disp_rect.pos = instance.pos
        self.disp_rect.size = instance.size

    def update_status_bar(self):
        sh = "[color=e6b800][SH][/color] " if self.shift_active else ""
        al = "[color=a680b8][AL][/color] " if self.alpha_active else ""
        hyp = "[color=3399ff][HYP][/color] " if self.hyp_active else ""
        m = "[color=000000][M][/color] " if self.memory_active else ""
        
        self.status_label.text = f"{sh}{al}{hyp}{m}[color=000000]RAD  MATH  DECI[/color]"

    def update_screen(self):
        before = self.expr_text[:self.cursor_pos]
        after = self.expr_text[self.cursor_pos:]
        self.display.text = f"{before}|{after}"

    def insert_text(self, text):
        self.expr_text = self.expr_text[:self.cursor_pos] + text + self.expr_text[self.cursor_pos:]
        self.cursor_pos += len(text)
        self.update_screen()
        
        if self.shift_active or self.alpha_active:
            self.shift_active = False
            self.alpha_active = False
            self.update_status_bar()

    def calculate(self):
        try:
            safe_env = {
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                'asin': lambda x: math.degrees(math.asin(x)),
                'acos': lambda x: math.degrees(math.acos(x)),
                'atan': lambda x: math.degrees(math.atan(x)),
                'sqrt': math.sqrt,
                'cbrt': lambda x: x**(1/3),
                'log10': math.log10,
                'log': math.log,
                'pi': math.pi,
                'e': math.e,
                'abs': abs
            }
            
            e = self.expr_text.replace('×', '*').replace('÷', '/')
            e = e.replace('³√', 'cbrt').replace('√', 'sqrt').replace('π', 'pi').replace('^', '**')
            e = e.replace('Sin⁻¹', 'asin').replace('Cos⁻¹', 'acos').replace('Tan⁻¹', 'atan')
            e = e.replace('Sin', 'sin').replace('Cos', 'cos').replace('Tan', 'tan')
            e = e.replace('Log', 'log10').replace('Ln', 'log')
            
            raw_res = eval(e, {"__builtins__": None}, safe_env)
            
            if isinstance(raw_res, float):
                if raw_res.is_integer():
                    res = str(int(raw_res))
                else:
                    res = f"{round(raw_res, 10):.10f}".rstrip('0').rstrip('.')
            else:
                res = str(raw_res)

            self.last_ans = res
            self.expr_text = res
            self.cursor_pos = len(res)
        except Exception:
            self.expr_text = "Syntax ERROR"
            self.cursor_pos = 0
        self.update_screen()

    def on_press(self, instance):
        t = instance.text
        
        if t == 'SHIFT':
            self.shift_active = not self.shift_active
            self.alpha_active = False
            self.update_status_bar()
            return
        elif t == 'ALPHA':
            self.alpha_active = not self.alpha_active
            self.shift_active = False
            self.update_status_bar()
            return
        elif t == 'hyp':
            self.hyp_active = not self.hyp_active
            self.update_status_bar()
            return
        elif t == 'M+':
            self.memory_active = True
            self.update_status_bar()
            return

        # التحكم في اتجاهات السهم
        if t == '<':
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                self.update_screen()
            return
        elif t == '>':
            if self.cursor_pos < len(self.expr_text):
                self.cursor_pos += 1
                self.update_screen()
            return
        elif t == '∧':
            self.cursor_pos = 0  # الانتقال لأول السطر
            self.update_screen()
            return
        elif t == '∨':
            self.cursor_pos = len(self.expr_text)  # الانتقال لآخر السطر
            self.update_screen()
            return

        if t == 'AC':
            self.expr_text = ""
            self.cursor_pos = 0
            self.shift_active = False
            self.alpha_active = False
            self.hyp_active = False
            self.update_screen()
            self.update_status_bar()
            return
        elif t == 'DEL':
            if self.cursor_pos > 0:
                self.expr_text = self.expr_text[:self.cursor_pos - 1] + self.expr_text[self.cursor_pos:]
                self.cursor_pos -= 1
                self.update_screen()
            return
        elif t == '=':
            self.calculate()
            self.shift_active = False
            self.alpha_active = False
            self.update_status_bar()
            return

        if self.shift_active:
            if t == 'Sin':
                self.insert_text('Sin⁻¹(')
            elif t == 'Cos':
                self.insert_text('Cos⁻¹(')
            elif t == 'Tan':
                self.insert_text('Tan⁻¹(')
            elif t == '∫dx':
                self.insert_text('³√(')
            elif t == '+':
                self.insert_text('π')
            elif t == '-':
                self.insert_text('e')
            else:
                self.insert_text(t)
            return

        if self.alpha_active:
            self.shift_active = False
            self.alpha_active = False
            self.update_status_bar()
            return

        if t in ['Sin', 'Cos', 'Tan', 'Log', 'Ln']:
            self.insert_text(f"{t}(")
        elif t == '√':
            self.insert_text('√(')
        elif t == 'x²':
            self.insert_text('^2')
        elif t == 'xⁿ':
            self.insert_text('^')
        elif t == 'x⁻¹':
            self.insert_text('^-1')
        elif t == '(-)':
            self.insert_text('-')
        elif t == 'Ans':
            self.insert_text(self.last_ans)
        elif t in ['MODE', '2nd', 'CALC', '∫dx', 'a/b', '°\'"', 'RCL', 'ENG', 'S⇔D', 'Exp']:
            pass
        else:
            self.insert_text(t)

if __name__ == '__main__':
    PerfectCasioCalc().run()
