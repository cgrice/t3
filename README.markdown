## Ticket Time Tracker - t<sup>3</sup>

t<sup>3</sup> is a simple cli app, which allows you to track time spent on 
tickets. It's tailored towards an agile workflow, with reports showing the 
number of points spent on a ticket, and total points over a certain timeframe 
(an iteration, in this case).

###Workflow

At the start of the iteration, you'll have a number of tickets to work on. First,
estimate how many points each ticket is worth:

    cg@home $ t3 estimate 143 1
    cg@home $ t3 estimate 156 3
    cg@home $ t3 estimate 200 4

Choose a ticket to work on, and punch in:

    cg@home $ t3 pi 156
    Not punched in to any tickets
    Punching in - ticket #156

Then go and work on some tickets - t3 will track your time spent. 

    cg@home $ t3 pi 200
    Punched out of ticket #156
    Punching in - ticket #200
    [Work]
    cg@home $ t3 pi 143
    Punched out of ticket #156
    Punching in - ticket #200

If you want to check how you're doing, just use t3 status:

    cg@home $ t3 status
     Ticket Time Tracker v0.1
    -----------------------------------------------
      Punched into ticket #143 for 0:1:4
    -----------------------------------------------
     Ticket status
    -----------------------------------------------
     Ticket	Time Spent	Points	Estimated
     156	0:0:37		0.0	0			
     200	0:0:38		0.0	0			
     143	0:1:4		0.0	0		<--	


At the end of an iteration, you can then check how you've done:

    cg@home $ t3 report
     Report
    -----------------------------------------------
      Total points estimated: 	8
      Total points done: 		0.0
      Total Difference: 		8.0
      Average difference: 		2.66666666667
    -----------------------------------------------
     Breakdown
    -----------------------------------------------
     Ticket	Points	Estimated	Diff
     143	0.0	1		1.0
     156	0.0	3		3.0
     200	0.0	4		4.0

You can then clean all tickets, ready for the next iteration. This cannot be
undone, so make sure you're ready to finish.

    cg@home $ t3 clean
	
However, you can still access historical data from previous iterations, using
t3 totals:

    cg@home $ t3 totals
    + Iteration ended 26/03/2009 at 12:13
         Ticket	Points
         20  	0.0
      Total: 0.0
    + Iteration ended 26/03/2009 at 12:14
         Ticket	Points
         20  	0.1
         100  	0.0
      Total: 0.1
    + Iteration ended 26/03/2009 at 12:16
         Ticket	Points
         123  	0.0
      Total: 0.0


    


    
