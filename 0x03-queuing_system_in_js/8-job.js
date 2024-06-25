import kue from 'kue';
const { Queue, Job } = kue;

// Create a Kue queue instance
const queue = kue.createQueue();


// Define the createPushNotificationsJobs function
function createPushNotificationsJobs(jobs, queue) {
    // Check if jobs is an array
    if (!Array.isArray(jobs)) {
        throw new Error('Jobs is not an array');
    }

    // Loop over the jobs in the jobs array
    jobs.forEach(jobData => {
        // Create a job in the queue for push_notification_code_3
        const job = queue.create('push_notification_code_3', jobData);

        // When a job is created
        job.on('enqueue', function() {
            console.log(`Notification job created: ${job.id}`);
        });

        // When a job is complete
        job.on('complete', function() {
            console.log(`Notification job ${job.id} completed`);
        });

        // When a job fails
        job.on('failed', function(errorMessage) {
            console.log(`Notification job ${job.id} failed: ${errorMessage}`);
        });

        // Job progress
        job.on('progress', function(progress) {
            console.log(`Notification job ${job.id} ${progress}% complete`);
        });

        // Save the job to the queue
        job.save();
    });
}

// Export the createPushNotificationsJobs function
export default createPushNotificationsJobs;