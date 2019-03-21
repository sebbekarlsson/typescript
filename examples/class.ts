class Person {
    message: string;
    
    function constructor(msg: string):void {
        this.message = msg; 
    };

    function say(): void {
        print(this.message);
    };
};

function main(argc: number, argv: string[]): number {
    print("Program started\n");
    let person = new Person("My message");
    person.say(person);
}
