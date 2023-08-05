import unittest, time
from queues.RedisQueue import RedisQueue

def domain_hash(req):
  from urlparse import urlparse
  return hash(urlparse(req).netloc)

class TestRedisQueue(unittest.TestCase):
  Q = RedisQueue()
  def test_client_counts(self):
      self.Q.redis.flushdb()
      Q1 = RedisQueue(allow_registration=True)
      self.assertEqual(1, Q1.number_clients())
      Q2 = RedisQueue(allow_registration=True)
      Q3 = RedisQueue(allow_registration=False)
      time.sleep(.3)
      self.assertEqual(2, Q1.number_clients())
      self.assertEqual(2, Q2.number_clients())

      Q1.registration_expiration_ms = 1
      Q2.registration_expiration_ms = 1
      Q1.register()
      Q2.register()

      time.sleep(0.1)
      #We see 1 queue even when there are 0
      #This is expected, it allows one to preload
      #crawler state, before starting workers.
      self.assertEqual(1, Q3.number_clients())
      self.assertEqual(1, Q3.number_clients())

  def test_send_location(self):
    self.Q.redis.flushdb()
    Q1 = RedisQueue(hash_function=domain_hash, allow_registration=True)
    Q2 = RedisQueue(hash_function=domain_hash, allow_registration=True)
    Q3 = RedisQueue(hash_function=domain_hash, allow_registration=True)
    links = ['http://a.com/', 'http://b.com/', 'http://c.com/']
    requests = [x for x in links]

    #Queues are empty
    self.assertIsNone(Q1.get())
    self.assertIsNone(Q2.get())
    self.assertIsNone(Q3.get())

    Q1.send(requests)

    #Everyone gets a link
    self.assertIn(Q1.get(), links)
    self.assertIn(Q2.get(), links)
    self.assertIn(Q3.get(), links)

    #Queues are empty again
    self.assertIsNone(Q1.get())
    self.assertIsNone(Q2.get())
    self.assertIsNone(Q3.get())

  def test_large_sets_links_and_queues(self):
    self.Q.redis.flushdb()
    links = ['http://'+str(i)+'.com' for i in range(0, 133)]
    Qs = [RedisQueue(hash_function=domain_hash, allow_registration=True) for i in range(0, 25)]
    Qs[0].send(links)
    num_retrieved = sum([len([link for link in Q]) for Q in Qs])
    self.assertEqual(133, num_retrieved)


  def test_rebalance(self):
    self.Q.redis.flushdb()
    links = ['http://'+str(i)+'.com' for i in range(0, 40)]

    Q1 = RedisQueue(hash_function=domain_hash, allow_registration=True)
    Q2 = RedisQueue(hash_function=domain_hash, allow_registration=True)
    Q3 = RedisQueue(hash_function=domain_hash, allow_registration=True)
    Q1.send(links)

    Q3.number_clients() #Force Q3 to track number of clients.

    Q1.registration_expiration_ms = 1
    Q2.registration_expiration_ms = 1
    Q1.register()
    Q2.register()

    time.sleep(0.1)
    Q3.number_clients() #force redistribution of dead queues
    linksP = [link for link in Q3]
    self.assertEqual(sorted([req for req in links]), sorted([req for req in linksP]))

if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestRedisQueue)
  unittest.TextTestRunner(verbosity=2).run(suite)
