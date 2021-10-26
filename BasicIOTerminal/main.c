#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define BUFFER_SIZE 1024
#define MAX_NAME_LENGTH 32
#define MAX_PATH_LENGTH 260

typedef struct
{
    char name[MAX_NAME_LENGTH];
    char path[MAX_PATH_LENGTH];
    int length;
    char timestamp[20]; // format: dd/mm/yyyy hh:mm:ss
    char **content;
} document;

typedef struct directory
{
    char name[MAX_NAME_LENGTH];
    char path[MAX_PATH_LENGTH];
    int num_dirs;
    int num_docs;
    struct directory **dirs;
    document **docs;
} directory;

directory *pwd;  // present working directory

void allocation_error()
{
    // fprintf stderr prints to stderr to terminal
    fprintf(stderr, "BIOT: allocation error\n");
    exit(EXIT_FAILURE);
}

// shell builtins

int BIOT_ls(char **args)
{
    int i = 0;
    while (pwd->dirs[i] != NULL)
    {
        printf("%s\n", pwd->dirs[i]->name);
    }
    return 1;
}

int BIOT_cd(char **args)
{
    // if no arguments are passed
    if (args[1] == NULL)
    {
        fprintf(stderr, "BIOT: expected argument to \"%s\"\n", args[0]);
        return 0;
    }
    else
    {
        char new_directory_path[MAX_PATH_LENGTH] = "";
        strcpy(new_directory_path, args[1]);
        
        // if new_directory_path is a full path name
        if (new_directory_path[0] == '~')
        {
        
        }
            // if new_directory_path is relative with ./ or ../
        else if (new_directory_path[0] == '.')
        {
        
        }
            // if new_directory_path is under current path
        else
        {
        
        }
        fprintf(stderr, "BIOT: could not find directory\n");
    }
    return 1;
}

int BIOT_help(char **args)
{
    
    return 1;
}

int BIOT_exit(char **args)
{
    
    return 1;
}

// dir_name = "[directory]/"
int sub_mkdir(directory *dir, char *dir_name)
{
    // find first NULL dir in dirs
    int j = 1;
    while (dir->dirs[j]->name[0] != '\0')    // BUG : random memory at dirs[j] != NULL
    {
        // if a directory already has dir_name
        if (strcmp(dir_name, dir->dirs[j]->name) == 0)
        {
            fprintf(stderr, "BIOT: directory %s already exists.\n", dir->dirs[j]->name);
            return 0;
        }
        j++;
        // if ran out of space for directories, reallocate space
        if (j == dir->num_dirs)
        {
            dir->dirs = realloc(dir->dirs, (dir->num_dirs + 32) * sizeof(directory));
        }
    }
    
    char new_path[MAX_PATH_LENGTH] = "";
    strcpy(new_path, dir->path);
    strcat(new_path, "/");
    strcat(new_path, dir_name);     // new_path = dir.path/dir_name
    
    directory new_directory = {
            "",
            "",
            32,
            32,
            NULL,
            NULL
    };
    
    strcpy(new_directory.name, dir_name);   // assign name
    strcpy(new_directory.path, new_path);   // assign path
    
    new_directory.dirs = calloc(32, sizeof(directory));   // allocate space for dirs
    new_directory.docs = calloc(32, sizeof(document));    // allocate space for docs
    
    new_directory.dirs[0] = dir->dirs[j];   // 1st directory ./ self
    new_directory.dirs[1] = dir;            // 2nd directory ../ super
    
    dir->dirs[j] = &new_directory;
    
    return 1;
}

int BIOT_mkdir(char **args)
{
    if (args[1] == NULL)
    {
        fprintf(stderr, "BIOT: expected argument to \"%s\"\n", args[0]);
        return 0;
    }
    else
    {
        int i = 1;
        
        // create a directory for each argument
        while (args[i] != NULL)
        {
            // check for a if argument is valid directory name
            int j = 0;
            while (args[i][j] != '\0')
            {
                if (!isalnum(args[i][j]))
                {
                    fprintf(stderr, "BIOT: arguments to %s must contain only alphanumeric characters or \n", args[0]);
                    return 0;
                }
                j++;
            }
            
            char *dir_name = args[i];
            sub_mkdir(pwd, dir_name);
            i++;
        }
    }
    return 1;
}

char *builtin_str[] = {
        "ls",
        "cd",
        "help",
        "exit",
        "mkdir"
};

int (*builtin_func[])(char **) = {
        &BIOT_ls,
        &BIOT_cd,
        &BIOT_help,
        &BIOT_exit,
        &BIOT_mkdir
};

int BIOT_num_builtins()
{
    return sizeof(builtin_str) / sizeof(char *);
}

// basic loop functions
char *BIOT_read_line()
{
    int buffer_size = BUFFER_SIZE;
    int position = 0;   // position in line
    char *buffer = malloc(buffer_size * sizeof(char));
    int c;  // current character is int bc EOF is an int
    
    // if the buffer points to null there was a problem allocating memory
    if (!buffer)
    {
        allocation_error();
    }
    
    while (1)
    {
        c = getchar();
        
        // if end of line reached, return buffer
        if (c == EOF || (char) c == '\n')
        {
            buffer[position] = '\0';
            return buffer;
        }
        else
        {
            buffer[position] = (char) c;
        }
        position++;
        
        // if more chars than buffer_size, reallocate
        if (position >= buffer_size)
        {
            buffer_size += BUFFER_SIZE;
            buffer = realloc(buffer, (size_t) buffer_size);
            if (!buffer)
            {
                allocation_error();
            }
        }
    }
}

#define BIOT_TOKEN_BUFFER_SIZE 64

char **BIOT_split_line(char *line)
{
    int buffer_size = BIOT_TOKEN_BUFFER_SIZE;
    int token_buffer_size = BIOT_TOKEN_BUFFER_SIZE;
    char **tokens = malloc(buffer_size * sizeof(char));
    char *token;
    
    if (!tokens)
    {
        allocation_error();
    }
    
    int c = 0, nc = 0, i = 0;
    while (line[c] != '\0')
    {
        nc = 0;
        token = calloc((size_t) token_buffer_size, sizeof(char));
        while (line[c] != ' ' && line[c] != '\t' && line[c] != '\r' && line[c] != '\n' && line[c] != '\a'
               && line[c] != '\0')
        {
            token[nc] = line[c];
            
            // if we read in \" then add up to next \" to token
            if (token[nc] == '"')
            {
                nc = -1;
                
                while (line[c] != '"')
                {
                    nc++;
                    c++;
                    
                    if (line[c] == '"')
                    {
                        break;
                    }
                    else if (line[c] == '\t' || line[c] == '\r' || line[c] == '\n' || line[c] == '\a' ||
                             line[c] == '\0')
                    {
                        fprintf(stderr, "BIOT: error: expected '\"'");
                        exit(EXIT_FAILURE);
                    }
                    
                    if (c >= token_buffer_size)
                    {
                        token_buffer_size += BIOT_TOKEN_BUFFER_SIZE;
                        token = realloc(token, token_buffer_size * sizeof(char));
                        if (!token)
                        {
                            allocation_error();
                        }
                    }
                    
                    token[nc] = line[c];
                }
                
            }
            
            nc++;
            c++;
            if (c >= token_buffer_size)
            {
                token_buffer_size += BIOT_TOKEN_BUFFER_SIZE;
                token = realloc(token, token_buffer_size * sizeof(char));
                if (!token)
                {
                    allocation_error();
                }
            }
        }
        tokens[i] = token;
        c++;
        i++;
    }
    return tokens;
}

int BIOT_execute(char **args)
{
    int i;
    
    if (args[0] == NULL)
    {
        // no command entered
        return 1;
    }
    
    // if command is builtin
    for (i = 0; i < BIOT_num_builtins(); i++)
    {
        if (strcmp(args[0], builtin_str[i]) == 0)
        {
            return (*builtin_func[i])(args);
        }
    }
    
    // TODO: if command is in bin
    
    
    // if command not found
    printf("Command \"%s\" not found.\nType \"help\" for a list of commands.", args[0]);
    return 1;
}

// main shell loop
// root - char * root directory string
void BIOT_loop(directory root)
{
    char *line; // line entered on terminal
    char **args;// args
    int status;
    
    do
    {
        printf("%s> ", pwd->path);
        line = BIOT_read_line();
        args = BIOT_split_line(line);
        status = BIOT_execute(args);
        
        free(line);
        free(args);
    } while (status);
}

int main(int argc, char **argv)
{
    // initialize / load config files
    directory *dirs = calloc(32, sizeof(directory));
    document *docs = calloc(32, sizeof(document));
    
    directory root = {
            "/",
            "/",
            32,
            32,
            &dirs,
            &docs
    };
    root.dirs[0] = &root;       // self
    root.dirs[1] = &root;       // super is self
    sub_mkdir(&root, "bin");    // binaries
    sub_mkdir(&root, "home");   // user home directories
    sub_mkdir(&root, "log");    // system logs directory
    sub_mkdir(&root, "proc");   // processes as files
    sub_mkdir(&root, "root");   // superuser root home directory
    sub_mkdir(&root, "sys");    // config
    
    pwd = &root;
    
    BIOT_ls(NULL);
    
    // run command loop
    BIOT_loop(root);
    
    free(dirs);
    free(docs);
    
    return EXIT_SUCCESS;
}
