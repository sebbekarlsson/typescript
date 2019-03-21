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
}
