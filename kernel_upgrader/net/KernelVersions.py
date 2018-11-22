from kernel_upgrader.net.PageInfo import Connection


class KernelVersions(Connection):
    def obtain_current_available_kernels(self):
        # type: () -> list
        releases = super(KernelVersions, self).getSoupObject().find("table", {"id": "releases"})
        versions = releases.find_all("tr")
        result = []
        for version in versions:
            parts = version.find_all("td")
            result.append({"release_type": parts[0].get_text(strip=True),
                           "release_version": parts[1].get("strong").get_text(strip=True),
                           "release_date": parts[2].get_text(strip=True),
                           "release_url": parts[3].get("a").get("href")})
        return result
