
use('test');

// Insert a few documents into the sales collection.
db.getCollection('db_test').insertMany([
    {
        "emp_id": 100,
        "emp_name": "Neel",
        "emp_ph": 989,
        "emp_gmail": "fdhs@gmail.com",
        "entry_time": 800,
        "leave_time": 1700,
        "over_time": 1 
    },
    {
        "emp_id": 101,
        "emp_name": "John Doe",
        "emp_ph": 123456,
        "emp_gmail": "johndoe@example.com",
        "entry_time": 830,
        "leave_time": 1630,
        "over_time": 0
    },
    {
        "emp_id": 102,
        "emp_name": "Alice Smith",
        "emp_ph": 987654,
        "emp_gmail": "alice.smith@example.com",
        "entry_time": 900,
        "leave_time": 1700,
        "over_time": 0
    },
    {
        "emp_id": 103,
        "emp_name": "Bob Johnson",
        "emp_ph": 654321,
        "emp_gmail": "bob.johnson@example.com",
        "entry_time": 815,
        "leave_time": 1715,
        "over_time": 1
    },
    {
        "emp_id": 104,
        "emp_name": "Emily Davis",
        "emp_ph": 987123,
        "emp_gmail": "emily.davis@example.com",
        "entry_time": 830,
        "leave_time": 1630,
        "over_time": 0
    },
    {
        "emp_id": 105,
        "emp_name": "Michael Wilson",
        "emp_ph": 123987,
        "emp_gmail": "michael.wilson@example.com",
        "entry_time": 845,
        "leave_time": 1645,
        "over_time": 0
    },
    {
        "emp_id": 106,
        "emp_name": "Samantha Brown",
        "emp_ph": 456789,
        "emp_gmail": "samantha.brown@example.com",
        "entry_time": 830,
        "leave_time": 1300,
        "over_time": -430
    },
    {
        "emp_id": 107,
        "emp_name": "David Wilson",
        "emp_ph": 987654,
        "emp_gmail": "david.wilson@example.com",
        "entry_time": 900,
        "leave_time": 1800,
        "over_time": 1
    },
    {
        "emp_id": 108,
        "emp_name": "Sarah Johnson",
        "emp_ph": 987123,
        "emp_gmail": "sarah.johnson@example.com",
        "entry_time": 815,
        "leave_time": 1630,
        "over_time": 0015
    },
    {
        "emp_id": 109,
        "emp_name": "Tom Smith",
        "emp_ph": 123987,
        "emp_gmail": "tom.smith@example.com",
        "entry_time": 830,
        "leave_time": 1645,
        "over_time": 0015
    }
]);


// Print a message to the output window.
console.log("Done inserting");
