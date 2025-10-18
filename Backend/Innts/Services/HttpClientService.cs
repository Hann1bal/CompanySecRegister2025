using System.Net;
using System.Text;

public class HttpClientService(IHttpClientFactory httpClient, IConfiguration configuration)
{
    private readonly IHttpClientFactory _clientFactory = httpClient;
    private readonly IConfiguration _configuration = configuration;

    public async Task<string> PostAsync(string endpoint = "", int id = default, string data = "")
    {
        var client = _clientFactory.CreateClient();
        HttpContent jStringContent = new StringContent(data, Encoding.UTF8, "application/json");
        var httpResponse = await client.PostAsync(
            string.Format(endpoint, _configuration["BaseUrl"], id),
            jStringContent).ConfigureAwait(false);
        if (httpResponse.StatusCode is not (HttpStatusCode.Forbidden or HttpStatusCode.Unauthorized)) return await httpResponse.Content.ReadAsStringAsync().ConfigureAwait(false);
        else return "";
    }
    public async Task<string> GetAsync(string endpoint = "", long id = default)
    {
        var client = _clientFactory.CreateClient();
        var message = new HttpRequestMessage
        {
            Method = HttpMethod.Get,
            RequestUri =
                new Uri(string.Format(endpoint, _configuration["BaseUrl"], id))
        };

        var httpResponse = await client.SendAsync(message).ConfigureAwait(false);
        if (httpResponse.StatusCode is not (HttpStatusCode.Forbidden or HttpStatusCode.Unauthorized or HttpStatusCode.NotFound))
            return await httpResponse.Content.ReadAsStringAsync().ConfigureAwait(false);
        return "";
    }

}