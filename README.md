# amp
Analytics Management Platform to manage BUILD info &amp; recruiting


Before using a new google form, please follow the steps below to ensure the Mongo DB is updated with the form submissions. 

1. Create a spreadsheet linked to the form.
2. Copy the spreadsheet ID from the url of the spreadsheet and paste it in the sheetID variable at the top of the google app script code.
3. Run the function named "setUpTrigger" to set up a trigger which listens for new form submissions.

After this, any new submissions to the form will be updated to the database.