import pygame
import pygame_gui


screen_info = pygame.display.Info()
manager = pygame_gui.UIManager((screen_info.current_w, screen_info.current_h), "custom_theme.json", starting_language='en', translation_directory_paths=['translations'])

top_bar = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (screen_info.current_w, 50)),
                                      starting_layer_height=1,
                                      manager=manager,
                                      object_id='#top_bar')

exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_info.current_w - 45, 5), (35, 35)),
                                           text="X",
                                           manager=manager,
                                           container=top_bar,
                                           object_id='#exit_button')

frame_left = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((0, 50), (screen_info.current_w // 5, screen_info.current_h - 50)),
    starting_layer_height=1,
    manager=manager,
    object_id='#frame')

frame_middle = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((screen_info.current_w // 5, 50), (
3 * screen_info.current_w // 5, screen_info.current_h - 50)),
                                           starting_layer_height=1,
                                           manager=manager,
                                           object_id='#frame')

frame_right = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((4 * screen_info.current_w // 5, 50), (
screen_info.current_w // 5, screen_info.current_h - 50)),
                                          starting_layer_height=1,
                                          manager=manager,
                                          object_id='#frame')

frame_middle_bottom = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,frame_middle.rect.height - 125),(frame_middle.rect.width-5, 150)),
                                           starting_layer_height=1,
                                           manager=manager,
                                           object_id='#frame',
                                           container = frame_middle
                                           )

frame_right_bottom = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,frame_right.rect.height - 125),(frame_right.rect.width-5, 150)),
                                           starting_layer_height=1,
                                           manager=manager,
                                           object_id='#frame',
                                           container = frame_right
                                           )

frame_left_bottom = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,frame_left.rect.height - 125),(frame_left.rect.width-5, 150)),
                                           starting_layer_height=1,
                                           manager=manager,
                                           object_id='#frame',
                                           container = frame_left
                                           )

frame_results = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,750),(frame_right.rect.width-5, 150)),
                                           starting_layer_height=1,
                                           manager=manager,
                                           object_id='frame',
                                           container = frame_right
                                           )


#top bar buttons


settings_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 0), (90, top_bar.rect.height-6)),
                                              text="translation.settings_btn",
                                              manager=manager,
                                              container=top_bar,
                                              object_id='#topbar_btn')

grid_nr_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((settings_btn.rect.width + 46, 0), (75, top_bar.rect.height-6)),
                                              text="translation.grids_btn",
                                              manager=manager,
                                              container=top_bar,
                                              object_id='#topbar_btn')

colors_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((settings_btn.rect.width + 46 + 71, 0), (75, top_bar.rect.height-6)),
                                              text="translation.colors_btn",
                                              manager=manager,
                                              container=top_bar,
                                              object_id='#topbar_btn')

recorder_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((settings_btn.rect.width + 46 + 71+71, 0), (90, top_bar.rect.height-6)),
                                              text="translation.recorder_btn",
                                              manager=manager,
                                              container=top_bar,
                                              object_id='#topbar_btn')

#interface buttons

drop_down_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((75, 400), (250, 50)),
                                              text="translation.drop_down_title",
                                              manager=manager,
                                              container=frame_right,
                                              object_id='#grid_size_title'
)
drop_down = pygame_gui.elements.UIDropDownMenu(
    relative_rect=pygame.Rect(((frame_right.rect.width - frame_right.rect.width // 1.2) / 2, 450),
                              (frame_right.rect.width // 1.2, 50)),
    manager=manager, options_list=['A*', 'Dijkstra', 'Greedy Best-First-Search', 'Breadth-First-Search', "Depth-First-Search"],
    starting_option='A*',
    container=frame_right,
    object_id='#drop_down'
    )

algorithm_error_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((110, 650), (170, 20)),
                                              text="translation.algorithm_error_label",
                                              manager=manager,
                                              container=frame_right,
                                              object_id='#error_msg'

)

run_algorithm = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(((frame_right.rect.width - frame_right.rect.width // 2) / 2, 675),
                              (frame_right.rect.width // 2, 50)),
    manager=manager,
    text="translation.run_algorithm",
    container=frame_right,
    object_id='#run_algorithm'
)

heuristic_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 500), (200, 50)),
                                              text="translation.heuristic_title",
                                              manager=manager,
                                              container=frame_right,
                                              object_id='#grid_size_title'
)
heuristic_options = pygame_gui.elements.UISelectionList(
    pygame.Rect(((frame_right.rect.width - frame_right.rect.width // 2) / 2 - 50, 550), (frame_right.rect.width // 2 - 70, 86)),
    item_list=['Manhattan',
               'Euclidean',
               'Octile',
               'Chebyshev'
               ],
    manager=manager,
    container=frame_right,
    object_id='#sel_list'
    )

diagonal_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((180, 500), (200, 50)),
                                              text="Execution options",
                                              manager=manager,
                                              container=frame_right,
                                              object_id='#grid_size_title'
)

diagonal_option = pygame_gui.elements.UISelectionList(
    pygame.Rect(((frame_right.rect.width - frame_right.rect.width // 2), 575), (frame_right.rect.width // 2 - 20, 26)),
    item_list=['translation.diagonal_option'],
    manager=manager,
    container=frame_right,
    object_id='#sel_list'
    )


spots_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((75, 300), (250, 50)),
                                              text="translation.spots_title",
                                              manager=manager,
                                              container=frame_left,
                                              object_id='#grid_size_title'
)


spots_options = pygame_gui.elements.UISelectionList(
        relative_rect=pygame.Rect(((frame_left.rect.width - frame_left.rect.width // 2) / 2 + 50, 350), (frame_left.rect.width // 2-100, 66)),
        item_list=['translation.spots_square',
                   'translation.spots_triangle',
                   'translation.spots_hexagon',
                   ],
        manager=manager,
        default_selection='translation.spots_square',
        container=frame_left,
        object_id='#sel_list'
)


arrow_coords_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((75, 425), (250, 50)),
                                              text="translation.arrow_coords_title",
                                              manager=manager,
                                              container=frame_left,
                                              object_id='#grid_size_title'
)

arrow_coord_options = pygame_gui.elements.UISelectionList(
        relative_rect=pygame.Rect(((frame_left.rect.width - frame_left.rect.width // 2) / 2, 475), (frame_left.rect.width // 2, 66)),
        item_list=['translation.show_arrows',
                   'translation.show_coords',
                   ],
        manager=manager,
        allow_multi_select = True,
        container=frame_left,
        object_id='#arrow_coord'
)


grid_size_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((100, 20), (200, 50)),
                                              text="translation.grid_size_title",
                                              manager=manager,
                                              container=frame_left,
                                              object_id='#grid_size_title'
)


grid_sizes = [5, 6, 9, 10, 12, 15, 18, 20, 25, 30, 36, 45, 50]

grid_sizes2 = [5, 10, 20, 25, 50]
grid_sizes3 = [5, 8, 10, 16, 20, 25, 40, 50]

grid_size_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((90, 70), (200, 20)),
        start_value=3,
        value_range=(0, len(grid_sizes) - 1),
        manager=manager,
        container=frame_left,
)

grid_size_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 90), (100, 50)),
                                              text=str(grid_sizes[int(grid_size_slider.get_current_value())]),
                                              manager=manager,
                                              container=frame_left
)


obstacles_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((75, 150), (250, 50)),
                                              text="translation.obstacles_title",
                                              manager=manager,
                                              container=frame_left,
                                              object_id='#grid_size_title'
)

maze_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(((frame_left.rect.width - frame_left.rect.width // 2) / 2, 190),
                              (frame_left.rect.width // 2, 50)),
    manager=manager,
    text="translation.maze_button",
    container=frame_left,
    object_id='#generate_button',
)


obstacles_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(((frame_left.rect.width - frame_left.rect.width // 2) / 2, 250),
                              (frame_left.rect.width // 2, 50)),
    manager=manager,
    text="translation.obstacles_button",
    container=frame_left,
    object_id='#generate_button',
)

clear_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(((frame_left.rect.width - frame_left.rect.width // 2) / 2, 675),
                              (frame_left.rect.width // 2, 50)),
    manager=manager,
    text="translation.clear_button",
    container=frame_left,
    object_id='#clear_button'
)






#logo
image_surface = pygame.image.load('logo.png')
image_surface = pygame.transform.scale(image_surface, (250,94))


image_surface_light = pygame.image.load('logo_light.png')
image_surface_light = pygame.transform.scale(image_surface_light, (250,94))

image = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect(((frame_middle_bottom.rect.width - 250)/2, 10), (250,94)),
    image_surface=image_surface,
    manager=manager,
    container=frame_middle_bottom,
)

#icon
corner_icon = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((0, 0), (top_bar.rect.height-6, top_bar.rect.height-6)),
                                              image_surface=pygame.image.load('icon.png'),
                                              manager=manager,
                                              container=top_bar,
                                              object_id='corner_icon')

#algorithm info

bfs_text = 'translation.bfs_text'

dfs_text = 'translation.dfs_text'

dijkstra_text = 'translation.dijkstra_text'

astar_text = 'translation.astar_text'

greedy_text = 'translation.greedy_text'



algo_info = pygame_gui.elements.UITextBox(
                                              "",
                                              relative_rect=pygame.Rect((0, 0), (frame_right.rect.width-6, 400)),
                                              manager=manager,
                                              container=frame_right,
                                              object_id='#algo_info')

# results


nodes_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 20), (120, 20)),
                                              text="translation.nodes_label",
                                              manager=manager,
                                              container=frame_results
)


nodes_entry = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((130, 20), (120, 20)),
                                              text="0",
                                              manager=manager,
                                              container=frame_results
)


steps_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 50), (100, 20)),
                                              text="translation.steps_label",
                                              manager=manager,
                                              container=frame_results
)

steps_entry = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((130, 50), (120, 20)),
                                              text="0",
                                              manager=manager,
                                              container=frame_results
)


length_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 80), (120, 20)),
                                              text="translation.length_label",
                                              manager=manager,
                                              container=frame_results
)


length_entry = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((130, 80), (120, 20)),
                                              text="0",
                                              manager=manager,
                                              container=frame_results
)

time_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 110), (100, 20)),
                                              text="translation.time_label",
                                              manager=manager,
                                              container=frame_results
)

time_entry = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((130, 110), (120, 20)),
                                              text="0",
                                              manager=manager,
                                              container=frame_results
)

delay_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((100, 550), (200, 50)),
                                              text="translation.delay_title",
                                              manager=manager,
                                              container=frame_left,
                                              object_id='#grid_size_title')



delay_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((90, 600), (200, 20)),
                                                          start_value=0,
                                                          value_range=(0, 500),
                                                          container=frame_left,
                                                          manager=manager)

delay_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 620), (100, 50)),
                                              text = str(delay_slider.get_current_value()) + " ms",
                                              manager=manager,
                                              container=frame_left
)


#names

dev_name = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((80, 5), (200, 50)),
                                              text="Developer: Pavel Gherciu",
                                              manager=manager,
                                              container=frame_right_bottom
)

coord_name = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((80, 55), (200, 50)),
                                              text="Coordinator: Vadim Strună",
                                              manager=manager,
                                              container=frame_right_bottom
)


english_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((100,10), (50, 40)),
    manager=manager,
    text="EN",
    container=frame_left_bottom,
    object_id='#en_button'
)

romanian_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((160,10), (50, 40)),
    manager=manager,
    text="RO",
    container=frame_left_bottom,
    object_id='#ro_button'
)

russian_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((220,10), (50, 40)),
    manager=manager,
    text="RU",
    container=frame_left_bottom,
    object_id='#ru_button'
)

bg_mode_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((120,60), (120, 50)),
    manager=manager,
    text="Light mode",
    container=frame_left_bottom,
    object_id='#bg_button'
)

grid2_algo1_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((175, 150), (200, 50)),
                                              text="",
                                              manager=manager,
                                              container=frame_middle
)


grid2_algo2_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((775, 150), (200, 50)),
                                              text="",
                                              manager=manager,
                                              container=frame_middle
)

grid3_algo1_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 0), (200, 25)),
                                              text="",
                                              manager=manager,
                                              container=frame_middle
)


grid3_algo2_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((725, 0), (200, 25)),
                                              text="",
                                              manager=manager,
                                              container=frame_middle
)

grid3_algo3_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((475, 440), (200, 25)),
                                              text="",
                                              manager=manager,
                                              container=frame_middle
)


grid4_algo1_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 0), (200, 25)),
                                              text="",
                                              manager=manager,
                                              container=frame_middle
)


grid4_algo2_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((725, 0), (200, 25)),
                                              text="",
                                              manager=manager,
                                              container=frame_middle
)

grid4_algo3_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 440), (200, 25)),
                                              text="",
                                              manager=manager,
                                              container=frame_middle
)

grid4_algo4_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((725, 440), (200, 25)),
                                              text="",
                                              manager=manager,
                                              container=frame_middle
)