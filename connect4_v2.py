import pygame
import sys
import moderngl
import numpy as np # Added moderngl import

from connect4_cli import Connect4
from minimax_ai import MiniMaxAI


# Initialization
pygame.init()
game = Connect4()
ai_player = MiniMaxAI(player_piece='\033[34m o \033[0m', level=3)


# --- CONSTANTS ---
# Board size
ROWS = 6
COLS = 7

# FONT
FONT = pygame.font.Font("VCR_OSD_MONO.ttf", 60)
FONT_PLAY_AGAIN = pygame.font.Font("VCR_OSD_MONO.ttf", 80)

# Colors (Retro-Futuristic Palette)
ALPHA = 128
BOARD_COLOR = (5, 10, 48)
CYAN_GLOW = (0, 255, 255)
MAGENTA_FURY = (255, 0, 255)
ELECTRIC_YELLOW = (255, 255, 0)
NEON_RED = (255, 49, 49)

SCANLINE_COLOR = (0, 0, 0, 30)
BACKGROUND_COLOR = (20, 30, 70) # For the empty slots

# Geometry
SQUARESIZE = 100 # The size of each square on the grid
RADIUS = int(SQUARESIZE / 2 - 5) # Radius of the circles (pieces)
PADDING = int(SQUARESIZE / 2) # Padding to center the circles

# Ghost surface
ghost_surface = pygame.Surface((RADIUS * 2, RADIUS * 2), pygame.SRCALPHA)
drop_speed = 8

# End Game
play_again = None
end_text = " "
end_text_color = CYAN_GLOW

# Screen dimensions calculated from board size
SCREEN_WIDTH = COLS * SQUARESIZE
SCREEN_HEIGHT = (ROWS + 1) * SQUARESIZE # +1 row for the top area
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE, pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Connect 4")

render_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA) # New render surface

ctx = moderngl.create_context(require=300) # moderngl context

# Vertices for a screen-filling quad
quad_vertices = [
    -1.0, -1.0,  0.0, 0.0,  # Bottom-left (x, y, u, v)
     1.0, -1.0,  1.0, 0.0,  # Bottom-right
    -1.0,  1.0,  0.0, 1.0,  # Top-left
     1.0,  1.0,  1.0, 1.0,  # Top-right
]
quad_buffer = ctx.buffer(data=np.array(quad_vertices, dtype='f4').tobytes()) # Using bytearray for float to bytes conversion

# Advanced CRT Shader Program
quad_program = ctx.program(
    vertex_shader="""
        #version 330 core
        in vec2 in_vert;
        in vec2 in_texcoord;
        out vec2 v_texcoord;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            v_texcoord = in_texcoord;
        }
    """,
    fragment_shader="""
        #version 330 core
        uniform sampler2D u_texture;
        uniform float u_time;
        uniform vec2 u_resolution;
        in vec2 v_texcoord;
        out vec4 f_color;

        void main() {
            vec2 uv = v_texcoord;

            // Barrel Distortion
            vec2 center = vec2(0.5, 0.5);
            vec2 tex_coords = uv - center;
            float r2 = dot(tex_coords, tex_coords);
            float f = 1.0 + r2 * 0.2; // Adjust 0.2 for more/less distortion
            uv = tex_coords * f + center;

            // Check if distorted UV is outside [0,1] range
            if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
                f_color = vec4(0.0, 0.0, 0.0, 1.0); // Black border
                return;
            }

            vec4 color = texture(u_texture, uv);

            // Scanlines (animated)
            float scanline_intensity = sin((uv.y * u_resolution.y + u_time * 10.0) * 3.14159 * 2.0) * 0.05 + 0.95;
            color.rgb *= scanline_intensity;

            // Vignette (darken edges)
            float vignette_strength = 0.6; // Adjust for more/less vignette
            float dist = distance(uv, center);
            float vignette = smoothstep(0.4, 1.0, dist) * vignette_strength;
            color.rgb *= (1.0 - vignette);

            f_color = color;
        }
    """
)
quad_vertex_array = ctx.vertex_array(quad_program, [(quad_buffer, '2f 2f', 'in_vert', 'in_texcoord')])


def draw_board(render_surface, board):
    for col in range(COLS):
        for row in range(ROWS):
            # Calculate the center of the circle
            center_x = col * SQUARESIZE + PADDING
            center_y = (row + 1) * SQUARESIZE + PADDING # +1 to leave space at the top

            # Determine the color based on the board state
            if board[row][col] == '   ':
                pass
            
            elif board[row][col] == '\033[31m o \033[0m': # Player 1 (user)
                color = MAGENTA_FURY
                pygame.draw.circle(render_surface, color, (center_x, center_y), RADIUS)

            else: # Player 2 (AI)
                color = ELECTRIC_YELLOW
                pygame.draw.circle(render_surface, color, (center_x, center_y), RADIUS)

def create_board_surface():
    board_size = (SCREEN_WIDTH, SCREEN_HEIGHT - SQUARESIZE)
    overlay_surface = pygame.Surface(board_size, pygame.SRCALPHA)
    overlay_surface.fill(BOARD_COLOR)
    hole_piece = (0, 0, 0, 0)

    for col in range(COLS):
        for row in range(ROWS):
            # Calculate the center of the circle
            center_x = col * SQUARESIZE + PADDING
            center_y = row  * SQUARESIZE + PADDING # +1 to leave space at the top

            pygame.draw.circle(overlay_surface, hole_piece, (center_x, center_y), RADIUS)
    
    return overlay_surface

def draw_board_overlay(overlay_surface):
    render_surface.blit(overlay_surface, (0, SQUARESIZE))

def update_game_state(game, piece_color):
    global end_text, end_text_color
    if game.check_win():
        game.game_over = True
        end_text_color = piece_color
        end_text = "RED WINS!" if end_text_color == MAGENTA_FURY else "YELLOW WINS!"

    elif game.check_draw():
        end_text = "GRIDLOCKED"

    else:
        game.switch_player()


# Main Game Loop
column = 0
hover_column = 0 
board_surface = create_board_surface()
start_time = pygame.time.get_ticks() # Added for shader time uniform
texture = None # Initialize texture to None

while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Cursor Position
        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]  # Get the x-coordinate of the mouse
            column = posx // SQUARESIZE # Calculate which column it is
            hover_column = column

        # Mouse Click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.game_over:
                continue

            row_index = game.get_next_open_row(column)

            if row_index is not None:

                render_surface.fill(BACKGROUND_COLOR)
                draw_board(render_surface, game.board)
                background_snapshot = render_surface.copy()

                # --- ANIMATION LOOP ---
                current_y = SQUARESIZE + PADDING                     # Calculate initial y position
                target_y = (row_index + 1) * SQUARESIZE + PADDING    # Calculate target y position
                center_x = column * SQUARESIZE + PADDING

                # Get the color of the piece in play
                piece_color = MAGENTA_FURY if game.current_player == '\033[31m o \033[0m' else ELECTRIC_YELLOW

                while current_y < target_y:
                    current_y = min(current_y + drop_speed, target_y)

                    # Refresh Screen
                    render_surface.blit(background_snapshot, (0, 0)) # Background
                    pygame.draw.circle(render_surface, piece_color, (center_x, current_y), RADIUS) # Piece falling
                    draw_board_overlay(board_surface) # Foreground
                    pygame.display.flip() # Changed 'pygame.display.update()' to 'pygame.display.flip()'
                    pygame.time.wait(10)
                
                game.drop_piece(column)

                # Update game state after player's move then switch player
                update_game_state(game, piece_color)

                # ---- AI's TURN ----
                if not game.game_over and \
                game.current_player == ai_player.player_piece:
                    pygame.time.wait(600)
                    # AI makes its move
                    ai_col =  ai_player.find_best_move(game.board)

                    render_surface.fill(BACKGROUND_COLOR)
                    draw_board(render_surface, game.board)
                    draw_board_overlay(board_surface)
                    background_snapshot = render_surface.copy()

                    # Animation
                    piece_color = MAGENTA_FURY if game.current_player == '\033[31m o \033[0m' else ELECTRIC_YELLOW
                    ai_row_index = game.get_next_open_row(ai_col)
                    if ai_row_index is not None and ai_col is not None:
                        ai_current_y = SQUARESIZE + PADDING
                        ai_target_y = (ai_row_index + 1) * SQUARESIZE + PADDING
                        ai_center_x = ai_col * SQUARESIZE + PADDING

                        while ai_current_y < ai_target_y:
                            ai_current_y = min(ai_current_y + drop_speed, ai_target_y)

                            render_surface.blit(background_snapshot, (0, 0))
                            pygame.draw.circle(render_surface, piece_color, (ai_center_x, ai_current_y), RADIUS)
                            draw_board_overlay(board_surface) 
                            pygame.display.flip() # Changed 'pygame.display.update()' to 'pygame.display.flip()'
                            pygame.time.wait(10)

                        game.drop_piece(ai_col) # Officially drop AI's piece
                        
                    # After AI's move, update game state and switch player
                    update_game_state(game, piece_color)

        else:
            continue


    # -- DRAWING --
    hover_row = SQUARESIZE - PADDING # top row
    center_x = hover_column * SQUARESIZE + PADDING 

    # GAME BOARD UPDATE
    render_surface.fill(BACKGROUND_COLOR) # Clear screen
    draw_board(render_surface, game.board) 
    draw_board_overlay(board_surface)

    # --- Main Drawing Logic ---
    if not game.game_over:
        # Ghost piece drawing
        hover_row = SQUARESIZE - PADDING # top row
        center_x = hover_column * SQUARESIZE + PADDING 
        ghost_surface.fill((0, 0, 0, 0)) # R, G, B, Alpha (0 for fully transparent)
        piece_color = MAGENTA_FURY if game.current_player == '\033[31m o \033[0m' else ELECTRIC_YELLOW
        ghost_piece = (piece_color[0], piece_color[1], piece_color[2], ALPHA)
        pygame.draw.circle(ghost_surface, ghost_piece, (RADIUS, RADIUS), RADIUS)
        render_surface.blit(ghost_surface, (center_x - RADIUS, hover_row - RADIUS)) # Changed 'screen' to 'render_surface'


    # --- End-Game Drawing Logic ---
    else:
        # END GAME MESSAGE
        end_message_surface = FONT.render(end_text, True, end_text_color)
        end_message_rect = end_message_surface.get_rect(center=(SCREEN_WIDTH/2, SQUARESIZE/2))
        render_surface.blit(end_message_surface, end_message_rect) # Changed 'screen' to 'render_surface'

        # --- PLAY AGAIN BUTTON ---
        play_again_rect = pygame.Rect(SCREEN_WIDTH*2/7, SCREEN_HEIGHT*2/7,
                                      SQUARESIZE*3, SQUARESIZE*2)
        # Button Background
        button_background = pygame.Surface(play_again_rect.size, pygame.SRCALPHA)
        button_background.fill((20, 30, 70, 150))

        # Button Borders
        pygame.draw.rect(button_background, NEON_RED, button_background.get_rect(), 8, 4, 4, 4, 4)

        # Text Rendering
        play_text_surface = FONT_PLAY_AGAIN.render("Play", True, NEON_RED)
        play_text_rect = play_text_surface.get_rect(center=(button_background.get_rect().centerx, button_background.get_rect().centery - 30))
        again_text_surface = FONT_PLAY_AGAIN.render("Again?", True, NEON_RED)
        again_text_rect = again_text_surface.get_rect(center=(button_background.get_rect().centerx, button_background.get_rect().centery + 30))
        button_background.blit(play_text_surface, play_text_rect)
        button_background.blit(again_text_surface, again_text_rect)

        render_surface.blit(button_background, play_again_rect.topleft) # Changed 'screen' to 'render_surface'

    # Update the Display (moderngl rendering)
    # Create a temporary RGB surface to blit the render_surface onto
    temp_surface = pygame.Surface(render_surface.get_size(), depth=24) # 24-bit RGB
    temp_surface.blit(render_surface, (0, 0))
    pixel_data = pygame.image.tostring(temp_surface, "RGBA")

    # Create or update the moderngl texture
    if texture is None:
        texture = ctx.texture(render_surface.get_size(), 4)
    texture.write(pixel_data)

    texture.use(0) # Use texture unit 0
    ctx.clear(0.0, 0.0, 0.0, 0.0) # Clear the moderngl context

    # Pass uniforms to the shader
    current_time = pygame.time.get_ticks() - start_time
    quad_program['u_time'].value = current_time / 1000.0  # Convert milliseconds to seconds
    quad_program['u_resolution'].value = render_surface.get_size()

    quad_vertex_array.render(moderngl.TRIANGLE_STRIP) # Render the quad with the texture
    pygame.display.flip() # Flip the display
