from kernel_upgrader.net.PageInfo import Connection


class KernelVersions(Connection):
    def obtain_current_available_kernels(self):
        # type: () -> list
        releases = super(KernelVersions, self).getSoupObject().find("table", {"id": "releases"})
        versions = releases.find_all("tr")
        result = []
        for version in versions:
            parts = version.find_all("td")
            if parts[3].find('a') is not None:
                result.append({"release_type": parts[0].get_text(strip=True).replace(':', ''),
                               "release_version": parts[1].get_text(strip=True),
                               "release_date": parts[2].get_text(strip=True),
                               "release_url": parts[3].find("a").get("href")})
        return result
