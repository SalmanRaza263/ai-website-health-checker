package ssl

import (
	"crypto/tls"
	"fmt"
	"time"
)

type SSLResult struct {
	Valid        bool      `json:"valid"`
	Issuer       string    `json:"issuer"`
	Subject      string    `json:"subject"`
	ValidFrom    time.Time `json:"valid_from"`
	ValidTo      time.Time `json:"valid_to"`
	DaysLeft     int       `json:"days_left"`
	Protocol     string    `json:"protocol"`
	CipherSuite  string    `json:"cipher_suite"`
}

func CheckSSL(host string) SSLResult {
	result := SSLResult{
		Valid: false,
	}

	conn, err := tls.Dial("tcp", fmt.Sprintf("%s:443", host), &tls.Config{
		InsecureSkipVerify: true,
	})
	if err != nil {
		return result
	}
	defer conn.Close()

	cert := conn.ConnectionState().PeerCertificates[0]
	protocol := conn.ConnectionState().Version
	cipher := conn.ConnectionState().CipherSuite

	result.Valid = true
	result.Issuer = cert.Issuer.CommonName
	result.Subject = cert.Subject.CommonName
	result.ValidFrom = cert.NotBefore
	result.ValidTo = cert.NotAfter
	result.DaysLeft = int(time.Until(cert.NotAfter).Hours() / 24)
	result.Protocol = getProtocolName(protocol)
	result.CipherSuite = tls.CipherSuiteName(cipher)

	return result
}

func getProtocolName(version uint16) string {
	switch version {
	case tls.VersionTLS10:
		return "TLS 1.0"
	case tls.VersionTLS11:
		return "TLS 1.1"
	case tls.VersionTLS12:
		return "TLS 1.2"
	case tls.VersionTLS13:
		return "TLS 1.3"
	default:
		return "Unknown"
	}
}