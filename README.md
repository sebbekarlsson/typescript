# typescript to c compiler
> Converts typescript to C.

## Example
### Input
> When given this typescript snippet:
```typescript
    class Dog {
        message: string;
        
        function constructor(): void {
            this.message = "Bark Bark\n"; 
        };

        function say(): void {
            print(this.message);
        };
    };

    class Cat {
        message: string;

        function constructor(): void {
            this.message = "Mew Mew\n";
        };

        function say(): void {
            print(this.message);
        };
    };

    function main(argc: number, argv: string[]): number {
        let dog = new Dog();
        dog.say();

        let cat = new Cat();
        cat.say();
    };
```

### Output
> The output will be this:
```c
    #include <stdio.h>
    #include <stdlib.h>

    typedef struct DOG_STRUCT {

      char *message;

      void (*constructor)(void *self);

      void (*say)(void *self);

    } Dog;

    void Dog_constructor(Dog *self) { self->message = "Bark Bark\n"; }

    void Dog_say(Dog *self) { printf(self->message); }

    Dog *init_Dog() {
      Dog *x = calloc(1, sizeof(struct DOG_STRUCT));

      x->message = calloc(1, sizeof(char *));

      x->constructor = Dog_constructor;

      x->say = Dog_say;

      return x;
    };


    typedef struct CAT_STRUCT {

      char *message;

      void (*constructor)(void *self);

      void (*say)(void *self);

    } Cat;

    void Cat_constructor(Cat *self) { self->message = "Mew Mew\n"; }

    void Cat_say(Cat *self) { printf(self->message); }

    Cat *init_Cat() {
      Cat *x = calloc(1, sizeof(struct CAT_STRUCT));

      x->message = calloc(1, sizeof(char *));

      x->constructor = Cat_constructor;

      x->say = Cat_say;

      return x;
    };

    int main(int argc, char **argv) {

      Dog *dog = init_Dog();

      Dog_constructor(dog);
      dog->say(dog);

      Cat *cat = init_Cat();

      Cat_constructor(cat);
      cat->say(cat);
    };
```
