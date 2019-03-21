class Person {
    message: string;
    
    function constructor(msg: string):void {
    
    };

    function say(message: string): void {
        print(message);
    };
};

function main(argc: number, argv: string[]): number {
    print("Program started\n");
    let person = new Person("My message");
}
