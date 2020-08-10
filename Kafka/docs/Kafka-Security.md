## Kafka - Security

1. Security in kafka would mostly cover the following
	1. Consumer to Broker communication
	2. Producer to Broker communication
	3. Broker to Broker communication
	4. Zookeeper to broker communication
&nbsp;

2. __Encryption and Authentication using SSL__
&nbsp;

	1. The communication between kafka brokers and clients and zookeeper can be secured by encryption and authentication using SSL. To implement SSL authentication and encryption, first you need to generate SSL keys and certificates for each kafka broker. Please follow the steps [here](https://kafka.apache.org/documentation/#security_ssl) to generate and sign the required certificates. You can also generate your own certificates and keys.
&nbsp;

	2. Configuration of kafka broker and kafka clients is also required. Here are the steps for [Broker config](https://kafka.apache.org/documentation/#security_configbroker) and [Client config](https://kafka.apache.org/documentation/#security_configclients).
	For configuration of python clients based on librdkafka refer [Python client config](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md).
&nbsp;

	3. For securing the zookeeper to broker communication, some additional config for zookeeper and broker need to done as mentioned [here](https://kafka.apache.org/documentation/#zk_authz_new_mtls).
&nbsp;

3. __Authentication using SASL__
&nbsp;

	1. Kafka uses the Java Authentication and Authorization Service for SASL configuration. Follow the steps for [JAAS config for Broker](https://kafka.apache.org/documentation/#security_jaas_broker) and [JAAS config for Clients](https://kafka.apache.org/documentation/#security_jaas_client).
&nbsp;

	2. SASL may be used with PLAINTEXT or SSL as the transport layer using the security protocol SASL_PLAINTEXT or SASL_SSL respectively. If SASL_SSL is used, then SSL must also be configured. To use SASL, follow the steps given for [SASL config for Broker](https://kafka.apache.org/documentation/#security_sasl_brokerconfig) and [SASL config for Client](https://kafka.apache.org/documentation/#security_sasl_clientconfig). Kafka supports the following SASL mechanisms - 
		1. [GSSAPI (Kerberos)](https://kafka.apache.org/documentation/#security_sasl_kerberos)
		2. [PLAIN](https://kafka.apache.org/documentation/#security_sasl_plain)
		3. [SCRAM-SHA-256](https://kafka.apache.org/documentation/#security_sasl_scram)
		4. [SCRAM-SHA-512](https://kafka.apache.org/documentation/#security_sasl_scram)
		5. [OAUTHBEARER](https://kafka.apache.org/documentation/#security_sasl_oauthbearer)
&nbsp;

	3. The default __SCRAM__ implementation in Kafka stores SCRAM credentials in Zookeeper and is suitable for use in Kafka installations where Zookeeper is on a private network. This needs to be considered when deploying in production environment.
&nbsp;

	4. The default __OAUTHBEARER__ implementation in Kafka creates and validates Unsecured JSON Web Tokens and is only suitable for use in non-production Kafka installations. OAUTHBEARER should be used in production enviromnments only with TLS-encryption to prevent interception of tokens. The default unsecured SASL/OAUTHBEARER implementation may be overridden (and must be overridden in production environments) using custom login and SASL Server callback handlers.
&nbsp;

	5. You can also enable multiple SASL mechanisms in a Kafka-broker. The configurations for the same is given [here](https://kafka.apache.org/documentation/#security_sasl_multimechanism).
&nbsp;

	6. To enable ZooKeeper SASL authentication on brokers, follow the steps listed at [ZooKeeper SASL Authentication](https://kafka.apache.org/documentation/#zk_authz_new_sasl).
&nbsp;

4. __Authentication using Delegation Tokens__
&nbsp;

	1. Delegation token based authentication is a lightweight authentication mechanism to complement existing SASL/SSL methods. Delegation tokens are shared secrets between kafka brokers and clients. Delegation tokens will help processing frameworks to distribute the workload to available workers in a secure environment without the added cost of distributing Kerberos TGT/keytabs or keystores when 2-way SSL is used.
	Typical steps for delegation token usage are
		1. User authenticates with the Kafka cluster via SASL or SSL, and obtains a delegation token. This can be done using Admin APIs or using kafka-delegation-tokens.sh script.
    	2. User securely passes the delegation token to Kafka clients for authenticating with the Kafka cluster.
    	3. Token owner/renewer can renew/expire the delegation tokens.
&nbsp;

	2. Follow the steps for [Token Management](https://kafka.apache.org/documentation/#security_token_management), [Creating Delegation Tokens](https://kafka.apache.org/documentation/#security_sasl_create_tokens) and [Token Authentication](https://kafka.apache.org/documentation/#security_token_authentication) for implementing this feature.

