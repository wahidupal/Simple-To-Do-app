import gooeypie as gp
import os

def add_new_task(event):
    """Adds a new task to the to do list when Enter is pressed"""
    if event.key['name'] == 'Return' and new_task_inp.text != '':
        todo_lst.add_item(new_task_inp.text)
        new_task_inp.clear()

def move_task(event):
    """Moves a task from one listbox to another"""
    if event.widget == todo_lst:
        # move the task from the todo list to the done list
        done_lst.add_item(todo_lst.remove_selected())
    else:
        # move the task from the done list to the todo list
        todo_lst.add_item(done_lst.remove_selected())


def delete_task(event):
    """Deletes a task from the todo list"""
    todo_lst.remove_selected()

def all_done(event):
    """Move all tasks from the todo list to the done list"""
    done_lst.items = done_lst.items + todo_lst.items
    todo_lst.items = []

def clear_all(events):
    """Removes all tasks from the done list"""
    done_lst.items = []

def load_tasks():
    """Loads tasks from the tasks file and populate the todo and done Listboxes"""
    try:
        with open('tasks.txt') as tasks_file:
            tasks = tasks_file.readlines()

        if tasks[0] != '\n':
            todo_lst.items = tasks[0].strip().split('\t')
        if tasks[1] != '\n':
            done_lst.items = tasks[1].strip().split('\t')
    
    except FileNotFoundError:
        #If the task file is not there, do nothing
        pass
    except IndexError:
        #if the file is not of the correct format, inform the user
        message = 'The task file could not be loaded due to incorrect format'
        app.alert('Could not load task file', message,'info')

def save_tasks():
    """Saves the todo and the done lists to the task file"""
    try:
        todos = '\t'.join(todo_lst.items)
        dones = '\t'.join(done_lst.items)

        with open('tasks.txt', 'w') as tasks_file:
            tasks_file.write(f'{todos}\n{dones}\n')
    
    except PermissionError:
        # Inform the user of the error and seek confirmation to exit
        message = f'Could not save tasks file in {os.getcwd()} due to permission error.\n\nAre you sure you want to exit?'
        return app.confirm_yesno('Can not save tasks file', message, 'warning')

    return True # without this line the todo app will not be closed. 

app = gp.GooeyPieApp('What is on the agenda today?')
app.width = 400


# Create all widgets

new_task_lbl = gp.Label(app, 'New Task')
new_task_inp = gp.Input(app)
todo_lbl = gp.Label(app, 'To do list')
todo_lst = gp.Listbox(app)
delete_task_btn = gp.Button(app, 'Delete Task', delete_task)
all_done_btn = gp.Button(app, 'All Done', all_done)
done_lbl = gp.Label(app, 'Done!')
done_lst = gp.Listbox(app)
clear_all_btn = gp.Button(app, 'Clear All', clear_all)

# Event listners
new_task_inp.add_event_listener('key_press', add_new_task)
todo_lst.add_event_listener('double_click', move_task)
done_lst.add_event_listener('double_click', move_task)

# Add widgets to windows
app.set_grid(5, 3) # adding rows and columns to the window
app.set_row_weights(0, 1, 0, 1, 0)
app.set_column_weights(0, 1, 1) # if I pass in 0 for the first column it will not grow and for the 2nd and 3rd column they will grow evenly since we pass in 1 for them 
app.add(new_task_lbl, 1, 1, align = 'right') # in here we have assigned "new task" lebel on the right on the first row and first column 
app.add(new_task_inp, 1, 2, column_span = 2, fill= True) # in we have assigned how long the input bar will be
app.add(todo_lbl, 2, 1, align = 'right')
app.add(todo_lst, 2, 2, column_span = 2, fill= True, stretch = True)
app.add(delete_task_btn, 3, 2, fill = True)
app.add(all_done_btn, 3, 3, fill = True)
app.add(done_lbl, 4, 1, align = 'right')
app.add(done_lst, 4, 2, column_span = 2, fill= True, stretch = True)
app.add(clear_all_btn, 5, 3, fill = True)

# Load any tasks and populate the listboxes
#app.on_open(load_tasks)
load_tasks()

# Save tasks when the app closes
app.on_close(save_tasks)

new_task_inp.focus() # in here we have specified where the text icon will be when the app is launched
app.run()