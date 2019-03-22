class Dog {
    message: string;
    
    function constructor(): void {
        this.message = "Bark Bark"; 
    };

    function say(): void {
        console.log(this.message);
    };
};

class Cat {
    message: string;

    function constructor(): void {
        this.message = "Mew Mew";
    };

    function say(): void {
        console.log(this.message);
    };
};

class Human {
    age: number;

    function constructor(age: number): void {
        this.age = age;
    };
};

function main(argc: number, argv: string[]): number {
    let dog = new Dog();
    dog.say();

    if (1) {
        let cat = new Cat();
        cat.say();
    } else {
        console.log("Nope");
    };

    let human = new Human(21);
    human.age = human.age + 14;
}
