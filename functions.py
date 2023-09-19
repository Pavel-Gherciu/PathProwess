from ui_elements import *
from ui_windows import *
import json


def change_theme():
    new_theme_data = {
        "#frame": {
            "colours": {
                "dark_bg": "#FFFFFF"
            }
        },
        "defaults": {
            "colours": {
                 "dark_bg": "#F4F4F4",
                 "normal_text": "#1C1C1C",
                 "hovered_text": "#1C1C1C",
                 "disabled_bg": "#2A2A2A"
            },
            "font": {
                "name": "OpenSans",
                "size": "12",
                "regular_resource": {
                      "package": "fonts",
                      "resource": "OpenSans.ttf"
                 }
            }
        },
        "#run_algorithm": {
            "colours":
                {
                    "normal_bg": "#661C1C",
                    "hovered_bg": "#a21515",
                    "active_bg": "#661C1C",
                    "normal_border": "#FFFFFF"
                },
            "misc":
                {
                    "shape": "rounded_rectangle",
                    "shape_corner_radius": "2",
                    "border_width": "1",
                    "shadow_width": "2"
                }
        },
        "#clear_button":
            {
                "colours":
                    {
                        "normal_bg": "#F4F4F4",
                        "hovered_bg": "#969696",
                        "active_bg": "#F4F4F4",
                        "normal_text": "#1C1C1C",
                        "hovered_text": "#1C1C1C"
                    },
                "misc":
                    {
                        "shape": "rounded_rectangle",
                        "shape_corner_radius": "2",
                        "border_width": "0",
                        "shadow_width": "2"
                    }
            },
        "#algo_info": {
            "colours": {
                "normal_text": "#1C1C1C",
                "hovered_text": "#1C1C1C"
            }
        },
        "#top_bar": {
            "colours": {
                "dark_bg": "#DBDEE3"
            }
        },
        "#topbar_btn":
            {
                "colours":
                    {
                        "normal_bg": "#DBDEE3",
                        "hovered_bg": "#0078F2",
                        "normal_text": "#1C1C1C",
                        "hovered_text": "#FFFFFF"
                    },
                "misc":
                    {
                        "shape": "rounded_rectangle",
                        "shape_corner_radius": "2",
                        "border_width": "0",
                        "shadow_width": "2"
                    }
            },
        "#drop_down":
            {
                "colours":
                    {
                        "normal_bg": "#DBDEE3",
                        "dark_bg": "#DBDEE3",
                        "hovered_bg": "#35393e"
                    },
                "misc":
                    {
                        "expand_direction": "down"
                    }
            },
        "#drop_down.#selected_option":
            {
                "colours":
                    {
                        "normal_bg": "#0078D4",
                        "hovered_bg": "#0078F2",
                        "normal_text": "#FFFFFF",
                        "hovered_text": "#FFFFFF"
                    },
                "misc":
                    {
                        "border_width": "1",
                        "open_button_width": "10"
                    }
            },
        "#drop_down.#drop_down_options_list.button":
            {
                "colours":
                    {
                        "normal_bg": "#F4F4F4",
                        "hovered_bg": "#969696"
                    }
            },
        "#sel_list":
            {
                "misc":
                    {
                        "expand_direction": "down"
                    },

                "colours":
                    {
                        "normal_bg": "#F4F4F4",
                        "hovered_bg": "#F4F4F4"
                    }
            },
        "#sel_list.@selection_list_item":
            {
                "colours":
                    {
                        "normal_bg": "#F4F4F4",
                        "hovered_bg": "#969696",
                        "normal_text": "#1C1C1C",
                        "hovered_text": "#FFFFFF"
                    },
            },
        "#arrow_coord.@selection_list_item": {
            "colours":
                {
                    "normal_bg": "#F4F4F4",
                    "hovered_bg": "#969696",
                    "normal_text": "#1C1C1C",
                    "hovered_text": "#FFFFFF"
                },
        },
        "#exit_button": {
            "colours":
                {
                    "normal_bg": "#661C1C",
                    "hovered_bg": "#a21515",
                    "active_bg": "#661C1C",
                }
        },
        "#en_button": {
            "colours": {
                "normal_bg": "#DBDEE3"
            }
        },
        "#ro_button":
            {
                "colours":
                    {
                        "normal_bg": "#DBDEE3"
                    }
            },
        "#ru_button":
            {
                "colours":
                    {
                        "normal_bg": "#DBDEE3"
                    }
            },
        "#bg_button": {
            "colours": {
                "normal_bg": "#DBDEE3"
            }
        },
        "#my_window": {
            "colours": {
                "dark_bg": "#FFFFFF"
            }
        },
        "#my_window.#title_bar": {
            "colours": {
                "normal_bg": "#F4F4F4",
                "normal_text": "#1C1C1C"
            }
        }
    }
    new_theme_data_json = json.dumps(new_theme_data)
    manager.ui_theme.update_theming(new_theme_data_json)
    manager.update(1)
    manager2.ui_theme.update_theming(new_theme_data_json)
    manager2.update(1)

def reset_theme():
    with open('custom_theme.json', 'r') as file:
        data = json.load(file)
    original_theme = json.dumps(data)
    manager.ui_theme.update_theming(original_theme)
    manager.update(1)
    manager2.ui_theme.update_theming(original_theme)
    manager2.update(1)


def update_color(color, surface):
    if surface == "closed":
        new_theme_data = {
            "#closed_node_surface": {
                "colours": {
                    "dark_bg": color
                }
            }
        }
    elif surface == "open":
        new_theme_data = {
            "#open_node_surface": {
                "colours": {
                    "dark_bg": color
                }
            }
        }
    elif surface == "path":
        new_theme_data = {
            "#path_surface": {
                "colours": {
                    "dark_bg": color
                }
            }
        }
    new_theme_data_json = json.dumps(new_theme_data)
    manager2.ui_theme.update_theming(new_theme_data_json)
    manager2.update(1)


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])