**Single UDP example**
[src](http://embeddedgmetric.googlecode.com/svn/trunk/gmetric3/java/gmetric3.java)

**Multicast and additional functionality**[src](http://embeddedgmetric.googlecode.com/svn/trunk/gmetric3/java/src/)

**Multicast project**
[documentation](http://embeddedgmetric.googlecode.com/svn/trunk/gmetric3/java/doc/)


**Usage**
(taken from main() /gmetric3/java/src/java/info/ganglia/GMonitor.java)
```
	/**
	 * Usage: java -jar GangliaMetrics.jar multicastAddress
         * Creates a Monitor and two testMetrics
         * Generates random values and increments metrics in a loop
         * Metrics are reported back at the specified interval and should show up in ganglia graphs
	 * 
	 * @param args
	 * @throws Exception
	 */
	public static void main(String args[]) throws Exception {
		final String host = InetAddress.getLocalHost().getHostName();
		if (args.length != 1) {
			System.out.println("Usage: java -jar GangliaMetrics.jar <multicast address>");
			return;
		}
		final String multicastAddress = args[0];
		if (null == multicastAddress || multicastAddress.trim().equals("")) {
			System.out.println("Usage: java -jar GangliaMetrics.jar <multicast address>");
			return;
		}
		GMonitor gmon = new GMonitor(multicastAddress, 30l);
		GMetricInteger testMetric = (GMetricInteger) gmon.createGMetric(host, "Ganglia Int Test", GMetric.VALUE_TYPE_INT, "count", GMetric.SLOPE_UNSPECIFIED, false);
		GMetricDouble testMetric2 = (GMetricDouble) gmon.createGMetric(host, "Ganglia Double Test ", GMetric.VALUE_TYPE_DOUBLE, "count2", GMetric.SLOPE_UNSPECIFIED, false);

		Random generator = new Random();
		int count = 0;
		double countDouble = 0;
		while(true) {
			Thread.sleep(5000);
			count = generator.nextInt(100);
			countDouble = generator.nextDouble() * 100;
			System.out.println(count);
			System.out.println(countDouble);
			testMetric.incrementValue(count);
			testMetric2.incrementValue(countDouble);
		}
	}
```