from sqs import SQS

def main():
    sqs = SQS()
    queue = 'https://sqs.us-east-1.amazonaws.com/637423519415/1227975517-resp-queue'
    # req_queue = 'https://sqs.us-east-1.amazonaws.com/637423519415/1227975517-req-queue'

    sqs.clear_sqs_queue(queue)


if __name__ == '__main__':
    main()