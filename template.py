from manim import*

# Variables
num_plane_shift = 3*LEFT
font_size = 22
big_font_size = 30


class Temp(Scene):
    # Background color
    config["background_color"] = GRAY_E

    def construct(self):
        # The width and height of the video's frame
        width = config["frame_width"]
        height = config["frame_height"]
        # Varibles 
        rect_height = 0.8*height
        rect_width = 0.4*width
        func_shift = 0.4*rect_height*UP + 0.5*LEFT
        panel_shift = 0.28*width*RIGHT

        # A function to make y = ax^2 + bx + c
        def makeFunc(a = 1, b = -2, c = -1, d = func_shift):
            str_a = "{:.2f}".format(a)
            str_b = "{:+.2f}".format(b)
            str_c = "{:+.2f}".format(c)
            func = MathTex(
                "y=" + str_a + "x^2" + str_b + "x" + str_c,
                font_size = big_font_size
            )
            p = 2
            func[0][p:p+len(str_a)].set_color(RED)
            p += len(str_a)+3
            func[0][p:p+len(str_b)-1].set_color(BLUE)
            p += len(str_b)+1
            func[0][p:].set_color(GREEN)
            func.shift(d)
            return func

        # A function to make a numberplane
        def makeNumPlane(y_range=[-11, 12], x_length=1.5, y_length=1.5, def_shift = num_plane_shift, font_size = font_size):
            x_start = int((y_range[0]+y_range[-1])/2 - abs(y_range[0]-y_range[-1])*x_length*width/y_length/height/2)
            x_end = int((y_range[0]+y_range[-1])/2 + abs(y_range[0]-y_range[-1])*x_length*width/y_length/height/2)
            
            plane = NumberPlane(
                y_range = y_range,
                x_range = [x_start-0.1, x_end+0.1],
                x_length = x_length*width,
                y_length = y_length*height,
                background_line_style={
                    "stroke_opacity": 0.2,
                    "stroke_color": YELLOW_A
                },
                axis_config = {
                    "color": WHITE,
                    "include_numbers": True,
                    "font_size": font_size
                }
            )
            
            origin = MathTex(r"O")
            origin.font_size = font_size
            origin.shift(plane.get_origin() + 0.2*DOWN + 0.2*RIGHT)
            
            coord_plane = VGroup(plane, origin)
            coord_plane.shift(def_shift)

            return coord_plane, plane
        
        # A function to make sliders
        def makeSlider(x_range = [-10, 10, 5], v = 0, line_color = WHITE, dot_color = WHITE, label = 'x', def_shift = ORIGIN):
            res = VGroup()
            line = NumberLine(
                x_range = x_range,
                length=0.8*rect_width, 
                include_ticks=True, 
                tick_size=0.08,
                stroke_width=5,
                include_numbers=True,
                font_size=24,
                color= line_color
            )
            dot = Dot(color = dot_color ).move_to(line.n2p(v))
            val = "{:.2f}".format(v)
            label = MathTex(label + "=" + val, font_size = big_font_size, color = dot_color).align_to(line, direction=LEFT).shift(0.5*UP+0.28*RIGHT)
            res.add(line, dot, label)
            res.shift(def_shift)
            return res

        # Value tracker a, b, c
        a = ValueTracker(1)
        b = ValueTracker(-2)
        c = ValueTracker(-1)

        # Coordinate system
        coord_plane1, plane1 = makeNumPlane()

        # Plot y = ax^2 + bx + c
        plot1 = always_redraw(
            lambda: plane1.plot(
                lambda x: a.get_value()*x**2 + b.get_value()*x + c.get_value(), 
                color = ORANGE
            )
        )

        # Rectangle :/
        rect1 = Rectangle(
            color = GRAY_B,
            height = rect_height,
            width = rect_width,
            fill_color = GRAY_E,
            fill_opacity = 1
        ).shift(panel_shift)

        # y = ax^2 + bx + c
        func = always_redraw(
            lambda: makeFunc(
                a = a.get_value(),
                b = b.get_value(),
                c = c.get_value(),
                d = func_shift + panel_shift
            )
        )

        # Sliders
        slidera = always_redraw(
            lambda: makeSlider(
                v = a.get_value(),
                line_color = RED_A,
                dot_color = RED_D,
                label = "a",
                def_shift =1.2*UP +panel_shift
            )
        )

        sliderb = always_redraw(
            lambda: makeSlider(
                v = b.get_value(),
                line_color = BLUE_A,
                dot_color = BLUE_D,
                label = "b",
                def_shift=0.3*DOWN +panel_shift
            )
        )

        sliderc = always_redraw(
            lambda: makeSlider(
                v = c.get_value(),
                line_color = GREEN_A,
                dot_color = GREEN_D,
                label = "c",
                def_shift= 1.8*DOWN + panel_shift
            )
        )
        
        panel = VGroup()
        panel.add(rect1, func, slidera, sliderb, sliderc)

        self.add(coord_plane1)
        self.add(plot1)
        self.add(panel)
        self.play(a.animate.set_value(5), run_time = 3)
        self.play(a.animate.set_value(0.5), run_time = 2)
        self.play(b.animate.set_value(2), run_time = 3)
        self.play(c.animate.set_value(-4), run_time = 1)

        