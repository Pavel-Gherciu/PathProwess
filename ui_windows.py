# because surfaces need to be blitted before windows added
import pygame
import pygame_gui
from ui_elements import manager

screen_info = pygame.display.Info()
manager2 = pygame_gui.UIManager((screen_info.current_w, screen_info.current_h), "custom_theme.json", starting_language='en', translation_directory_paths=['translations'])


class CustomUIWindow(pygame_gui.elements.UIWindow):
    def kill(self):
        # Instead of killing this window, just hide it.
        self.hide()

grids_window = CustomUIWindow(rect=pygame.Rect((100, 100), (400, 400)),
                                      manager=manager2,
                                      window_display_title='translation.grids_window',
                                      object_id='#my_window',
                                      resizable=True,
                                      )

grids_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 20), (400, 20)),
                                              text="translation.grids_title",
                                              manager=manager2,
                                              container=grids_window
)

grid_nr_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((100, 50), (150, 20)),
        start_value=2,
        value_range=(2, 4),
        manager=manager2,
        container=grids_window,
)

grid_nr_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 50), (50, 20)),
                                              text=str(grid_nr_slider.get_current_value()),
                                              manager=manager2,
                                              container=grids_window
)

grid_algorithms_option = pygame_gui.elements.UISelectionList(
    pygame.Rect((100, 100), (150, 107)),
    item_list=['A*', "Dijkstra", "BFS", "Greedy", "DFS"],
    manager=manager2,
    container=grids_window,
    allow_multi_select = True,
    object_id='#sel_list'
    )

grid_nr_error_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((90, 220), (170, 20)),
                                              text="translation.grid_nr_error",
                                              manager=manager2,
                                              container=grids_window,
                                              object_id='#error_msg'

)

generate_grids_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((100, 250), (150, 50)),
    manager=manager2,
    text="translation.generate_grids",
    container=grids_window,
    object_id='#generate_button'
)



results_window = CustomUIWindow(rect=pygame.Rect((600, 200), (700, 600)),
                                      manager=manager2,
                                      window_display_title='translation.results_window',
                                      object_id='#my_window',
                                      resizable=True,
                                      )



# need to fix resize
results_box = pygame_gui.elements.UITextBox(
                                              '<font face=fira_code size=2.5 color=#FFFFFF>'
                                              ''
                                              '<img src="images/plot1.png" padding="5px 10px 0px 50px">'
                                              '<img src="images/plot2.png" padding="5px 10px 0px 50px">'
                                              '<img src="images/plot3.png" padding="5px 10px 0px 50px">'
                                              '<img src="images/plot4.png" padding="5px 10px 0px 50px">'
                                              '<img src="images/plot5.png" padding="5px 10px 0px 50px">'
                                              '</font>',
                                              relative_rect=pygame.Rect((0, 0), (results_window.rect.width - 32, results_window.rect.height - 60)),
                                              manager=manager2,
                                              container=results_window,
                                              object_id='results_box')


colors_window = CustomUIWindow(rect=pygame.Rect((100, 100), (400, 400)),
                                      manager=manager2,
                                      window_display_title='Color picker',
                                      object_id='#my_window',
                                      resizable=True,
                                      )

closed_node_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 50), (120, 40)),
                                              text="Closed node",
                                              manager=manager2,
                                              container=colors_window,
                                              object_id='#topbar_btn'
)

image_surface = pygame.Surface((100, 100))

closed_node_surface = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((180, 30), (80,80)),
                                      manager=manager2,
                                      container=colors_window,
                                      object_id='#closed_node_surface'
                                    )


open_node_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 150), (120, 40)),
                                              text="Open node",
                                              manager=manager2,
                                              container=colors_window,
                                              object_id='#topbar_btn'
)


open_node_surface = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((180, 130), (80,80)),
                                      manager=manager2,
                                      container=colors_window,
                                      object_id='#open_node_surface'
                                    )


path_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 250), (120, 40)),
                                              text="Path",
                                              manager=manager2,
                                              container=colors_window,
                                              object_id='#topbar_btn'
)

path_surface = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((180, 230), (80,80)),
                                      manager=manager2,
                                      container=colors_window,
                                      object_id='#path_surface'
                                    )

