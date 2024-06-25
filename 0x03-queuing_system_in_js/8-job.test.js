import { expect } from 'chai';
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job.js';

const queue = createQueue();


describe('createPushNotificationsJobs', () => {
    it('should throw an error if jobs is not an array', () => {
        const invalidJobs = 'not an array';

        expect(() => createPushNotificationsJobs(invalidJobs, queue)).to.throw('Jobs is not an array');
    });

    it('should create jobs in the queue', () => {
        const jobs = [
            { data: { message: 'Hello World 1' } },
            { data: { message: 'Hello World 2' } },
            { data: { message: 'Hello World 3' } }
        ];

        createPushNotificationsJobs(jobs, queue);

        expect(queue.testMode.jobs.length).to.equal(jobs.length);

        // You can also check if the job types and data match
        jobs.forEach((job, index) => {
            expect(queue.testMode.jobs[index].type).to.equal('push_notification_code_3');
            expect(queue.testMode.jobs[index].data).to.deep.equal(job.data);
        });
    });
});        