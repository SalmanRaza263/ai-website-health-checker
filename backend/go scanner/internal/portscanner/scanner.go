package portscanner

import (
	"fmt"
	"net"
	"strconv"
	"strings"
	"time"
)

type ScanResult struct {
	Port     int    `json:"port"`
	Protocol string `json:"protocol"`
	State    string `json:"state"`
	Service  string `json:"service"`
}

func ScanHost(host string, ports []int) []ScanResult {
	var results []ScanResult

	for _, port := range ports {
		address := fmt.Sprintf("%s:%d", host, port)
		conn, err := net.DialTimeout("tcp", address, time.Second*2)

		if err == nil {
			conn.Close()
			results = append(results, ScanResult{
				Port:     port,
				Protocol: "tcp",
				State:    "open",
				Service:  getServiceName(port),
			})
		}
	}

	return results
}

func getServiceName(port int) string {
	services := map[int]string{
		20: "FTP-data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
		53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC", 123: "NTP",
		135: "MSRPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
		445: "SMB", 993: "IMAPS", 995: "POP3S", 3306: "MySQL",
		5432: "PostgreSQL", 6379: "Redis", 27017: "MongoDB",
	}

	if service, exists := services[port]; exists {
		return service
	}
	return "Unknown"
}