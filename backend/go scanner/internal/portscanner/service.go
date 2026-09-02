package service

import (
	"fmt"
	"net"
	"strings"
)

type ServiceInfo struct {
	Name    string `json:"name"`
	Version string `json:"version"`
}

func DetectService(host string, port int) ServiceInfo {
	info := ServiceInfo{
		Name:    "Unknown",
		Version: "Unknown",
	}

	switch port {
	case 22:
		info.Name = "SSH"
	case 80:
		info.Name = "HTTP"
		if banner := getBanner(host, port); banner != "" {
			if strings.Contains(banner, "nginx") {
				info.Version = extractVersion(banner, "nginx")
			} else if strings.Contains(banner, "Apache") {
				info.Version = extractVersion(banner, "Apache")
			}
		}
	case 443:
		info.Name = "HTTPS"
	case 3306:
		info.Name = "MySQL"
	case 5432:
		info.Name = "PostgreSQL"
	case 6379:
		info.Name = "Redis"
	}

	return info
}

func getBanner(host string, port int) string {
	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", host, port))
	if err != nil {
		return ""
	}
	defer conn.Close()

	buffer := make([]byte, 1024)
	conn.SetReadDeadline(net.TimeoutError{})
	n, _ := conn.Read(buffer)

	if n > 0 {
		return string(buffer[:n])
	}
	return ""
}

func extractVersion(banner string, service string) string {
	parts := strings.Split(banner, " ")
	for i, part := range parts {
		if strings.Contains(strings.ToLower(part), strings.ToLower(service)) {
			if i+1 < len(parts) {
				return strings.TrimSpace(parts[i+1])
			}
		}
	}
	return "Unknown"
}