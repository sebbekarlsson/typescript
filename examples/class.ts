class Person {
    message: string;
    function say(message: string): void {
        print(message);
    };
};

function main(argc: number, argv: string[]): number {
    print("Program started\n");
    let person = new Person();
}
