Delegate = Contract
public delegate void MyEventHandler(int value);

// This means: any method attatched MUST look like this:
void AnyMethodName(int someNumber) { }

Event = Mailing List
public event MyEventHandler OnThresholdReached;
// This creates a list of methods to call when event happens

Raise Event = Send to all
if (OnThresholdReached != null){
    OnThresholdReached(currentValue);
}
// "Send currentValue to everyone on the mailing list"

Why use Events?
Without events(Tightly coupling):
ex:
you want to tell your friends about a party:
- you call alia directly
- you call balia directly
- you call calia directly
problem: you need to know everyon's number

With Events (Decoupled):
you post on a group chat:
- everyone who joined that chat sees it
- you don't need to know who's listening
- people can join or leave anytime

