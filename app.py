import hashlib
from flask import Flask, request

app = Flask(__name__)


def _process_work(buffer, iterations):
    output = hashlib.sha512(buffer).digest()
    for i in range(iterations - 1):
        output = hashlib.sha512(output).digest()
    return output


class WorkQueue:
    def __init__(self):
        self.work_items = {}
        self.work_id_counter = 0

    def enqueue_work(self, buffer, iterations):
        work_id = self._generate_work_id()
        self.work_items[work_id] = {
            'buffer': buffer,
            'iterations': iterations,
            'status': 'pending'
        }
        return work_id

    def pull_completed_work(self, top):
        completed_work = []
        for work_id, work_item in self.work_items.items():
            if work_item['status'] == 'completed':
                completed_work.append({
                    'work_id': work_id,
                    'result': _process_work(work_item['buffer'], work_item['iterations'])
                })
                if len(completed_work) == top:
                    break
        return completed_work

    def _generate_work_id(self):
        self.work_id_counter += 1
        return str(self.work_id_counter)


work_queue = WorkQueue()


@app.route('/enqueue', methods=['PUT'])
def enqueue():
    iterations = int(request.args.get('iterations'))
    buffer = request.data
    work_id = work_queue.enqueue_work(buffer, iterations)
    return work_id


@app.route('/pullCompleted', methods=['POST'])
def pull_completed():
    top = int(request.args.get('top'))
    completed_work = work_queue.pull_completed_work(top)
    return {'completed_work': completed_work}


if __name__ == '__main__':
    app.run()
